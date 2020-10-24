from setuptools import setup
from setuptools_rust import Binding, RustExtension

extras = {}
extras["testing"] = ["pytest"]

setup(
    name="tokenizers_zh",
    version="0.8.1",
    description="Fast and Customizable Tokenizers",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="NLP tokenizer BPE transformer deep learning",
    author="Anthony MOI",
    author_email="anthony@huggingface.co",
    url="https://github.com/huggingface/tokenizers",
    license="Apache License 2.0",
    rust_extensions=[RustExtension("tokenizers_zh.tokenizers", binding=Binding.PyO3)],
    extras_require=extras,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=[
        "tokenizers_zh",
        "tokenizers_zh.models",
        "tokenizers_zh.decoders",
        "tokenizers_zh.normalizers",
        "tokenizers_zh.pre_tokenizers",
        "tokenizers_zh.processors",
        "tokenizers_zh.trainers",
        "tokenizers_zh.implementations",
    ],
    package_data={
        "tokenizers_zh": ["py.typed", "__init__.pyi"],
        "tokenizers_zh.models": ["py.typed", "__init__.pyi"],
        "tokenizers_zh.decoders": ["py.typed", "__init__.pyi"],
        "tokenizers_zh.normalizers": ["py.typed", "__init__.pyi"],
        "tokenizers_zh.pre_tokenizers": ["py.typed", "__init__.pyi"],
        "tokenizers_zh.processors": ["py.typed", "__init__.pyi"],
        "tokenizers_zh.trainers": ["py.typed", "__init__.pyi"],
        "tokenizers_zh.implementations": ["py.typed"],
    },
    zip_safe=False,
)
