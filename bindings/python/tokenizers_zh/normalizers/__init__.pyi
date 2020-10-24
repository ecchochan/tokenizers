from typing import Optional, List

class Normalizer:
    """ Base class for all normalizers

    This class is not supposed to be instantiated directly. Instead, any implementation of a
    Normalizer will return an instance of this class when instantiated.
    """

class BertNormalizer(Normalizer):
    """ BertNormalizer

    Takes care of normalizing raw text before giving it to a Bert model.
    This includes cleaning the text, handling accents, chinese chars and lowercasing
    """

    def __init__(
        self,
        clean_text: Optional[bool] = True,
        handle_chinese_chars: Optional[bool] = True,
        separate_numbers: Optional[bool] = False,
        strip_accents: Optional[bool] = None,
        lowercase: Optional[bool] = True,
        special_chars: Optional[str] = "",
        opencc_config: Optional[str] = "s2t",
        zh_norm: Optional[bool] = False,
        handle_simpl: Optional[bool] = False,
    ) -> None:
        """ Instantiate a BertNormalizer with the given options.

        Args:
            clean_text: (`optional`) boolean:
                Whether to clean the text, by removing any control characters
                and replacing all whitespaces by the classic one.

            handle_chinese_chars: (`optional`) boolean:
                Whether to handle chinese chars by putting spaces around them.

            separate_numbers: (`optional`) boolean:
                Whether to put spaces around numbers so they get split

            strip_accents: (`optional`) boolean:
                Whether to strip all accents. If this option is not specified (ie == None),
                then it will be determined by the value for `lowercase` (as in the original Bert).

            lowercase: (`optional`) boolean:
                Whether to lowercase.

            special_chars: (`optional`) string:
                Chars that spaces will be put around so they get split

            zh_norm: (`optional`) boolean:
                Chars that will be replaced by custom mapping

            handle_simpl: (`optional`) boolean:
                Chars that will be normalized by simplified characters

        Returns:
            Normalizer
        """
        pass

class NFD(Normalizer):
    """ NFD Unicode Normalizer """

    def __init__(self) -> None:
        """ Instantiate a new NFD Normalizer """
        pass

class NFKD(Normalizer):
    """ NFKD Unicode Normalizer """

    def __init__(self) -> None:
        """ Instantiate a new NFKD Normalizer """
        pass

class NFC(Normalizer):
    """ NFC Unicode Normalizer """

    def __init__(self) -> None:
        """ Instantiate a new NFC Normalizer """
        pass

class NFKC(Normalizer):
    """ NFKC Unicode Normalizer """

    def __init__(self) -> None:
        """ Instantiate a new NFKC Normalizer """
        pass

class Sequence(Normalizer):
    """ Allows concatenating multiple other Normalizer as a Sequence.

    All the normalizers run in sequence in the given order
    """

    def __init__(self, normalizers: List[Normalizer]) -> None:
        """ Instantiate a new normalization Sequence using the given normalizers

        Args:
            normalizers: List[Normalizer]:
                A list of Normalizer to be run as a sequence
        """
        pass

class Lowercase(Normalizer):
    """ Lowercase Normalizer """

    def __init__(self) -> None:
        """ Instantiate a new Lowercase Normalizer """
        pass

class Strip(Normalizer):
    """ Strip normalizer """

    def __init__(self, left: bool = True, right: bool = True) -> Normalizer:
        pass

def unicode_normalizer_from_str(normalizer: str) -> Normalizer:
    """
    Instanciate unicode normalizer from the normalizer name
    :param normalizer: Name of the normalizer
    :return:
    """
    pass
