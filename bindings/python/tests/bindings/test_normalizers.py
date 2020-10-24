import pickle

from tokenizers_zh import Tokenizer
from tokenizers_zh.models import BPE
from tokenizers_zh.normalizers import Normalizer, BertNormalizer, Sequence, Lowercase, Strip


class TestBertNormalizer:
    def test_instantiate(self):
        assert isinstance(BertNormalizer(), Normalizer)
        assert isinstance(BertNormalizer(), BertNormalizer)
        assert isinstance(pickle.loads(pickle.dumps(BertNormalizer())), BertNormalizer)

    def test_strip_accents(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = BertNormalizer(
            strip_accents=True, lowercase=False, handle_chinese_chars=False, 
            separate_numbers=False, clean_text=False, zh_norm=False
        )

        output = tokenizer.normalize("Héllò")
        assert output == "Hello"

    def test_handle_chinese_chars(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = BertNormalizer(
            strip_accents=False, lowercase=False, handle_chinese_chars=True, 
            separate_numbers=False, clean_text=False, zh_norm=False
        )

        output = tokenizer.normalize("你好")
        assert output == " 你  好 "

    def test_handle_separate_numbers(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = BertNormalizer(
            strip_accents=False, lowercase=False, handle_chinese_chars=True, 
            separate_numbers=True, clean_text=False, zh_norm=False
        )

        output = tokenizer.normalize("你好123 is 123")
        assert output == " 你  好  1  2  3  is  1  2  3 "

    def test_clean_text(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = BertNormalizer(
            strip_accents=False, lowercase=False, handle_chinese_chars=False, 
            separate_numbers=False, clean_text=True, zh_norm=False
        )

        output = tokenizer.normalize("\ufeffHello")
        assert output == "Hello"

    def test_lowercase(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = BertNormalizer(
            strip_accents=False, lowercase=True, handle_chinese_chars=False, 
            separate_numbers=False, clean_text=False, zh_norm=False
        )

        output = tokenizer.normalize("Héllò")
        assert output == "héllò"

    def test_special_chars(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = BertNormalizer(
            strip_accents=False, lowercase=False, handle_chinese_chars=False, 
            separate_numbers=False, clean_text=False, 
            special_chars="$%", zh_norm=False
        )

        output = tokenizer.normalize("$100 and 0.5% $$ %%")
        assert output == " $ 100 and 0.5 %   $  $   %  % ", output


    def test_zh_norm(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = BertNormalizer(
            strip_accents=False, lowercase=False, handle_chinese_chars=False, 
            separate_numbers=False, clean_text=False, zh_norm=True
        )

        output = tokenizer.normalize("系列 聯系 « 联系 𠱁 氹 𥱊 栄 梊 𠹌 <n> \x00" )
        assert output == "系列 聯系 << 聯繫  o氹 氹 席 榮 折木  o能 <n>  ", output

        output = tokenizer.normalize("头部" )
        assert output == "頭部", output

class TestSequence:
    def test_instantiate(self):
        assert isinstance(Sequence([]), Normalizer)
        assert isinstance(Sequence([]), Sequence)
        assert isinstance(pickle.loads(pickle.dumps(Sequence([]))), Sequence)

    def test_can_make_sequences(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = Sequence([Lowercase(), Strip()])

        output = tokenizer.normalize("  HELLO  ")
        assert output == "hello"


class TestLowercase:
    def test_instantiate(self):
        assert isinstance(Lowercase(), Normalizer)
        assert isinstance(Lowercase(), Lowercase)
        assert isinstance(pickle.loads(pickle.dumps(Lowercase())), Lowercase)

    def test_lowercase(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = Lowercase()

        output = tokenizer.normalize("HELLO")
        assert output == "hello"


class TestStrip:
    def test_instantiate(self):
        assert isinstance(Strip(), Normalizer)
        assert isinstance(Strip(), Strip)
        assert isinstance(pickle.loads(pickle.dumps(Strip())), Strip)

    def test_left_strip(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = Strip(left=True, right=False)

        output = tokenizer.normalize("  hello  ")
        assert output == "hello  "

    def test_right_strip(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = Strip(left=False, right=True)

        output = tokenizer.normalize("  hello  ")
        assert output == "  hello"

    def test_full_strip(self):
        tokenizer = Tokenizer(BPE())
        tokenizer.normalizer = Strip(left=True, right=True)

        output = tokenizer.normalize("  hello  ")
        assert output == "hello"
