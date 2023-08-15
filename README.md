# LangScriptID
Detect the script of text based on ISO 15924.
- The codes were sourced from [Wikipedia ISO_15924](https://en.wikipedia.org/wiki/ISO_15924).
- Unicode ranges were extracted from [Unicode Character Database](https://www.unicode.org/Public/15.0.0/ucd/Scripts.txt).


## Install
```bash
pip3 install LangScriptID@git+https://github.com/kargaranamir/LangScriptID
```

## Usage

```python
from LangScriptID import get_script_predictor
sp = get_script_predictor()
```

```python
sp('これは日本人です')
>> ('Hira', 0.625, {'details': {'Hira': 0.625, 'Hani': 0.375}, 'tie': False, 'interval': 0.25})
```

```python
sp('This is Latin')
>> ('Latn', 1.0, {'details': {'Latn': 1.0}, 'tie': False, 'interval': 1})
```

```python
sp('මේක සිංහල')
>> ('Sinh', 1.0, {'details': {'Sinh': 1.0}, 'tie': False, 'interval': 1})
```

```python
sp('𝄞𝄫  𒊕𒀸')
>> ('Xsux', 0.5, {'details': {'Xsux': 0.5, 'Zyyy': 0.5}, 'tie': True, 'interval': 0.0})
```


## Citation
If you use any part of this library in your research, please cite it using the following BibTex entry. 

```
@misc{langscriptid,
  author = {Kargaran, Amir Hossein},
  title = {LangScriptID Python Library},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/kargaranamir/LangScriptID}},
}
```


## Related Sources
- [List of Unicode characters - Wikipedia](https://en.wikipedia.org/wiki/List_of_Unicode_characters)
- [Lightweight Plain-Text Editor for macOS - CotEditor](https://github.com/coteditor/CotEditor/blob/main/CotEditor/Sources/Unicode.UTF32.CodeUnit%2BBlockName.swift)
- [The Cygwin Terminal – terminal emulator for Cygwin, MSYS, and WSL - mintty](https://github.com/mintty/mintty/blob/master/src/scripts.t)
- [ISO_15924 Wikipedia](https://en.wikipedia.org/wiki/ISO_15924)
- [Unicode Character Database (Blocks) - Unicode](http://www.unicode.org/Public/4.1.0/ucd/Blocks.txt)
- [Unicode Character Database (Scripts) - Unicode](https://www.unicode.org/Public/15.0.0/ucd/Scripts.txt)
- [A free, web-based font editor, focusing on font design hobbyists. - Glyphr-Studio-1 ](https://github.com/glyphr-studio/Glyphr-Studio-1/blob/master/dev/js/lib_unicode_blocks.js)
- [Kotlin - JetBrains](https://github.com/JetBrains/kotlin/blob/master/libraries/stdlib/native-wasm/src/kotlin/text/regex/AbstractCharClass.kt)
- [UNIX-like reverse engineering framework and command-line toolset - radare2](https://github.com/radareorg/radare2/blob/master/libr/util/utf8.c)
- [FreeOrion Game](https://github.com/freeorion/freeorion/blob/master/GG/src/UnicodeCharsets.cpp)
- [DOMinator - Firefox](https://github.com/wisec/DOMinator/blob/master/gfx/thebes/gfxFontUtils.cpp)
- [SHSans-derived CJK font family - glow-sans](https://github.com/welai/glow-sans/blob/master/src/utils/code-range.js)
- [Unicode Subset Bitfields - Microsoft](https://learn.microsoft.com/en-us/windows/win32/intl/unicode-subset-bitfields)
- [Stops - FAIR NLLB FB](https://github.com/facebookresearch/stopes/blob/main/stopes/pipelines/monolingual/utils/predict_script.py)
- [Gradient Boosting on Decision Trees - catboost](https://github.com/catboost/catboost/blob/master/contrib/python/fonttools/fontTools/unicodedata/Blocks.py)
- [Blender](https://github.com/blender/blender/blob/main/source/blender/blenfont/intern/blf_glyph.cc)
- [Unicode Wikipedia](https://en.wikipedia.org/wiki/Unicode_block)
