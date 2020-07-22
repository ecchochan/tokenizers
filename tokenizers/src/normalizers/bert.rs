use crate::tokenizer::{NormalizedString, Normalizer, Result as _Result};
extern crate opencc_rust;
use serde::{
    de::{MapAccess, Visitor},
    ser::SerializeStruct,
    Deserialize, Deserializer, Serialize, Serializer,
};
use unicode_categories::UnicodeCategories;
use fnv::FnvHashSet;
use fnv::FnvHashMap;

use opencc_rust::{OpenCC,DefaultConfig};


/// A wrapper for OpenCC such that it is serializable
//
//   TODO :: Make config customizable
//
pub struct _OpenCC {
    opencc: OpenCC
}
impl _OpenCC {
    pub fn new() -> Self {
        let opencc = OpenCC::new(DefaultConfig::S2HK).unwrap();
        _OpenCC {
            opencc
        }
    }
}


/// Checks whether a character is whitespace
fn is_whitespace(c: char) -> bool {
    // These are technically control characters but we count them as whitespace
    if c == '\t' || c == '\n' || c == '\r' {
        true
    } else {
        c.is_whitespace()
    }
}

/// Checks whether a character is a control character
fn is_control(c: char) -> bool {
    // These are technically control characters but we count them as whitespace
    if c == '\t' || c == '\n' || c == '\r' {
        false
    } else {
        // The definition of `is_control` here is quite large and contains also
        // Cc, Cf, Cn or Co
        // cf. https://unicode.org/reports/tr44/ (Table 12)
        c.is_other()
    }
}

/// Checks whether a character is chinese
/// This defines a "chinese character" as anything in the CJK Unicode block:
///   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
///
/// Note that the CJK Unicode block is NOT all Japanese and Korean characters,
/// despite its name. The modern Korean Hangul alphabet is a different block,
/// as is Japanese Hiragana and Katakana. Those alphabets are used to write
/// space-separated words, so they are not treated specially and handled
/// like for all of the other languages.
fn is_chinese_char(c: char) -> bool {
    match c as usize {
        0x4E00..=0x9FFF => true,
        0x3400..=0x4DBF => true,
        0x20000..=0x2A6DF => true,
        0x2A700..=0x2B73F => true,
        0x2B740..=0x2B81F => true,
        0x2B920..=0x2CEAF => true,
        0xF900..=0xFAFF => true,
        0x2F800..=0x2FA1F => true,
        _ => false,
    }
}

/// match for numbers
fn is_number(c: char) -> bool {
    match c as usize {
        0x30..=0x39 => true,
        _ => false,
    }
}

#[derive(Serialize, Deserialize)]
pub struct BertNormalizer {
    /// Whether to do the bert basic cleaning:
    ///   1. Remove any control characters
    ///   2. Replace all sorts of whitespace by the classic one ` `
    clean_text: bool,
    /// Whether to put spaces around chinese characters so they get split
    handle_chinese_chars: bool,
    /// Whether to put spaces around numbers so they get split
    separate_numbers: bool,
    /// Whether to strip accents
    strip_accents: Option<bool>,
    /// Whether to lowercase the input
    lowercase: bool,
    /// Whether to check to special chars
    check_special_chars: bool,
    /// Chars that spaces will be put around so they get split
    special_char_mapping: FnvHashSet<char>,
    /// Whether to normalize chinese characters
    zh_norm: bool,
    /// Chars that will be replaced by custom mapping
    zh_norm_mapping: FnvHashMap<char, String>,
    /// openCC Object
    opencc: _OpenCC,
}

impl Default for BertNormalizer {
    fn default() -> Self {
        Self {
            clean_text: true,
            handle_chinese_chars: true,
            separate_numbers: false,
            strip_accents: None,
            lowercase: true,
            check_special_chars: false,
            special_char_mapping: FnvHashSet::default(),
            zh_norm: false,
            zh_norm_mapping: FnvHashMap::default(),
            opencc: _OpenCC::new()
        }
    }
}

impl BertNormalizer {
    pub fn new(
        clean_text: bool,
        handle_chinese_chars: bool,
        separate_numbers: bool,
        strip_accents: Option<bool>,
        lowercase: bool,
        special_chars: String,
        zh_norm: bool,
    ) -> Self {
        let mut special_char_mapping: FnvHashSet<char> = FnvHashSet::default();
        let mut zh_norm_mapping: FnvHashMap<char, String> = FnvHashMap::default();
        for c in special_chars.chars() {
            special_char_mapping.insert(c);
        }
        let mut check_special_chars = false;
        if special_chars.len() > 0 {
            check_special_chars = true;
        }

        if zh_norm {
            for line in include_str!("zh_char2str_mapping.txt").lines() {
                let mut pair = line.split('\t');
                let left = pair.next().unwrap().chars().next().unwrap();
                let right = pair.next().unwrap();
                zh_norm_mapping.insert(left, right.to_string());
            }
        
        }

        let opencc = _OpenCC::new();


        BertNormalizer {
            clean_text,
            handle_chinese_chars,
            separate_numbers,
            strip_accents,
            lowercase,
            check_special_chars,
            special_char_mapping,
            zh_norm,
            zh_norm_mapping,
            opencc
        }
    }

    fn do_clean_text(&self, normalized: &mut NormalizedString) {
        normalized
            .filter(|c| !(c as usize == 0 || c as usize == 0xfffd || is_control(c)))
            .map(|c| if is_whitespace(c) { ' ' } else { c });
    }

    fn do_handle_separate_chars(&self, 
                                normalized: &mut NormalizedString, 
                                handle_chinese_chars: bool, 
                                separate_numbers: bool, 
                                check_special_chars: bool, 
                                special_char_mapping: &FnvHashSet<char>,
                                zh_norm: bool,
                                zh_norm_mapping: &FnvHashMap<char, String>,
                            ) {
        let mut new_chars: Vec<(char, isize)> = vec![];
        normalized.for_each(|c| {
            if zh_norm {
                // 
                // The added normalization for Chinese character replacement
                // 
                match zh_norm_mapping.get(&c) {
                    Some(rep) => {
                        rep.chars().enumerate().for_each(|(i, c2)| {
                            if (handle_chinese_chars && is_chinese_char(c2)) || 
                               (separate_numbers && is_number(c2)) || 
                               (check_special_chars && special_char_mapping.contains(&c2))  {
                                new_chars.extend(&[(' ', 1), (c2, if i == 0 {0} else {1}), (' ', 1)]);
                            } else {
                                new_chars.push((c2, if i == 0 {0} else {1}));
                            }
                        });
                    },
                    None => {
                        if (handle_chinese_chars && is_chinese_char(c)) || 
                           (separate_numbers && is_number(c)) || 
                           (check_special_chars && special_char_mapping.contains(&c))  {
                            new_chars.extend(&[(' ', 1), (c, 0), (' ', 1)]);
                        } else {
                            new_chars.push((c, 0));
                        };

                    },

                }

            }else {
                // 
                // The original implementation + separate numbers and special chars
                // 
                if (handle_chinese_chars && is_chinese_char(c)) || 
                   (separate_numbers && is_number(c)) || 
                   (check_special_chars && special_char_mapping.contains(&c))  {
                    new_chars.extend(&[(' ', 1), (c, 0), (' ', 1)]);
                } else {
                    new_chars.push((c, 0));
                }
                
            }
        });
        normalized.transform(new_chars.into_iter(), 0);
    }

    fn do_strip_accents(&self, normalized: &mut NormalizedString) {
        normalized.nfd().filter(|c| !c.is_mark_nonspacing());
    }

    fn do_lowercase(&self, normalized: &mut NormalizedString) {
        normalized.lowercase();
    }
}

#[typetag::serde]
impl Normalizer for BertNormalizer {
    fn normalize(&self, mut normalized: &mut NormalizedString) -> _Result<()> {
        
        //
        // Use OpenCC to normalize for Simplfied Chinese
        //
            
        if self.zh_norm {
            // 
            // fix unknown error from OpenCC for having '\u{00}' in the string
            // 
            
            let normalized_str = normalized.get();
            let normalized_str_arg;
            if normalized_str.chars().any(|c| c == '\u{00}') {
                normalized_str_arg = normalized_str.replace("\u{00}", " ");
            }else {
                normalized_str_arg = normalized_str.to_string();
            }

            normalized.set_normalized(self.opencc.opencc.convert(normalized_str_arg));
        }
        if self.clean_text {
            self.do_clean_text(normalized);
        }
        if self.handle_chinese_chars || self.separate_numbers || self.check_special_chars || self.zh_norm {
            self.do_handle_separate_chars(&mut normalized, 
                                          self.handle_chinese_chars, 
                                          self.separate_numbers, 
                                          self.check_special_chars, 
                                          &self.special_char_mapping, 
                                          self.zh_norm, 
                                          &self.zh_norm_mapping);
        }
        let strip_accents = self.strip_accents.unwrap_or(self.lowercase);
        if strip_accents {
            self.do_strip_accents(normalized);
        }
        if self.lowercase {
            self.do_lowercase(normalized);
        }

        Ok(())
    }
}


impl Serialize for _OpenCC {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let model = serializer.serialize_struct("OpenCC", 2)?;
        model.end()
    }
}

impl<'de> Deserialize<'de> for _OpenCC {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        deserializer.deserialize_struct("OpenCC", &[], OpenCCVisitor)
    }
}

struct OpenCCVisitor;
impl<'de> Visitor<'de> for OpenCCVisitor {
    type Value = _OpenCC;

    fn expecting(&self, fmt: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(fmt, "struct OpenCC")
    }

    fn visit_map<V>(self, mut _map: V) -> std::result::Result<Self::Value, V::Error>
    where
        V: MapAccess<'de>,
    {
        Ok(_OpenCC::new())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn basic() {
        let norm = BertNormalizer::new(
            true,
            true,
            true,
            Some(true),
            true,
            "".to_string(),
            true,
        );
        let mut input = NormalizedString::from("系列 聯系 « 联系 𠱁 氹 𥱊 栄 梊 𠹌 <n> \u{00}");
        let _ = norm.normalize(&mut input).unwrap();
        assert_eq!(
            input.get(),
            " 系  列   聯  系  <<  聯  繫   o 氹   氹   席   榮   折   o 能  <n>  "
        );
    }
}
