__version__ = "0.8.1"

from typing import Tuple, Union, Tuple, List

Offsets = Tuple[int, int]

TextInputSequence = str
PreTokenizedInputSequence = Union[List[str], Tuple[str]]
TextEncodeInput = Union[TextInputSequence, Tuple[TextInputSequence, TextInputSequence]]
PreTokenizedEncodeInput = Union[
    PreTokenizedInputSequence, Tuple[PreTokenizedInputSequence, PreTokenizedInputSequence]
]

InputSequence = Union[TextInputSequence, PreTokenizedInputSequence]
EncodeInput = Union[TextEncodeInput, PreTokenizedEncodeInput]

from .tokenizers_zh import Tokenizer, Encoding, AddedToken
from .tokenizers_zh import decoders
from .tokenizers_zh import models
from .tokenizers_zh import normalizers
from .tokenizers_zh import pre_tokenizers
from .tokenizers_zh import processors
from .tokenizers_zh import trainers
from .implementations import (
    ByteLevelBPETokenizer,
    CharBPETokenizer,
    SentencePieceBPETokenizer,
    BertWordPieceTokenizer,
)
