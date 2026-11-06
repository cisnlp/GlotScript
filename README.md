# GlotScript

GlotScript has two parts:

- **GlotScript-Resource**: the writing systems of the languages of ISO 639-3 (8,035 listed, 7,503 with a main script), as ISO 15924 codes.
- **GlotScript-Tool**: a Python library that finds the script (writing system) of a text, of each of its parts and
  of each of its words, for all scripts of Unicode 17.0.0.

## Install

```bash
pip3 install GlotScript
# or the latest version from GitHub:
pip3 install GlotScript@git+https://github.com/cisnlp/GlotScript
```

## Tool

| Function | Short name | What it returns |
|---|---|---|
| `get_script_predictor()` | `sp` | the main script of a text, its share, and the share of every script |
| `separate_script(text)` | `sc` | the characters of each script, with the text's spaces |
| `script_segments(text)` | `ss` | the text cut into single-script parts, with character offsets |
| `word_scripts(text)` | `ws` | the main script of every word |
| `script_covers(writing_system, script)` | | whether a writing system such as `Jpan` uses a script such as `Hira` |

All of them share one table of the scripts of Unicode characters, built the first time it is needed.

### Script of a text

```python
from GlotScript import sp

sp('これは日本人です')
>> ('Hira', 0.625, {'details': {'Hira': 0.625, 'Hani': 0.375}, 'tie': False, 'interval': 0.25})

sp('This is Latin')[:2]
>> ('Latn', 1.0)
```

The text is scored after removing white space, ASCII punctuation and ASCII digits
(`get_script_predictor(replace_punctuation=True, replace_digits=True)`, the settings of `sp`).

### Characters of each script

```python
from GlotScript import sc

sc("Hello Salut سلام 你好 こんにちは שלום مرحبا")
>> {'Latn': 'Hello Salut     ', 'Hebr': '     שלום ', 'Arab': '  سلام    مرحبا', 'Hani': '   你好   ', 'Hira': '    こんにちは  '}
```

Every script keeps all the spaces of the text, so its words stay in order.

### Parts of a text

```python
from GlotScript import ss

ss("Hello Salut سلام 你好")
>> [('Latn', 0, 11, 'Hello Salut'), ('Zyyy', 11, 12, ' '), ('Arab', 12, 16, 'سلام'), ('Zyyy', 16, 17, ' '), ('Hani', 17, 19, '你好')]
```

Each part is `(script, start, end, text)` with `text[start:end]` equal to the part, and the parts cover the whole
text in order. Combining marks (`Zinh`) take the script of the character before them. Spaces, digits and punctuation
(`Zyyy`) join the parts around them when both have the same script, and are their own part otherwise;
`ss(text, common="separate")` keeps every run of them separate.

### Script of every word

```python
from GlotScript import ws

ws("I love 你好, ok!")
>> [('I', 'Latn'), ('love', 'Latn'), ('你好,', 'Hani'), ('ok!', 'Latn')]
```

A word's script is the most frequent one among its characters, not counting spaces, digits and punctuation
(combining marks count for the character before them); ties go to the script seen first. A word with no other
characters is `Zyyy`.

### Writing systems of language labels

Some ISO 15924 codes name writing systems that combine Unicode scripts (`Jpan` = Han + Hiragana + Katakana, `Kore` =
Hangul + Han, `Hanb` = Han + Bopomofo, `Hrkt` = Hiragana + Katakana) or vary one (`Hans`, `Hant`).
`script_covers` tells whether a writing system, for example the script part of a language label such as `jpn_Jpan`,
uses a script found by `sp`, `ss` or `ws`; `COMPOSITE_SCRIPTS` lists these codes.

```python
from GlotScript import script_covers

script_covers('Jpan', 'Hira'), script_covers('Kore', 'Hani'), script_covers('Latn', 'Cyrl')
>> (True, True, False)
```

### Special codes

- `Zinh` (Inherited): characters such as combining marks that take the script of the character before them. A few
  Arabic marks of this block are counted as Arabic.
- `Zyyy` (Common): characters used by many scripts, such as spaces, digits, punctuation and most symbols.
- `Zzzz` (Unknown): code points outside every script, and `U+FFFD` (the replacement character).

Script codes follow [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924); the character ranges come from the
[Unicode Character Database](https://www.unicode.org/Public/17.0.0/ucd/Scripts.txt) (Unicode 17.0.0).

### Updating to a new Unicode version

The character ranges are generated into `GlotScript/ranges.py` from the Unicode Character Database
(`Scripts.txt` and `PropertyValueAliases.txt`), with GlotScript's own adjustments listed in `GlotScript/update.py`
(Arabic harakat counted as Arabic, `U+FFFD` as `Zzzz`):

```bash
python -m GlotScript.update --version 18.0.0   # or latest
python -m GlotScript.update --check            # does ranges.py match the data?
python tests/test_glotscript.py
```

## Resource

Which writing systems is each language written in?

| Language | CORE | AUXILIARY |
|---|---|---|
| Turkish (tur) | Latn | Arab, Cyrl, Grek |
| Thai (tha) | Thai | Latn |
| Vietnamese (vie) | Latn | Hani |

The full list is in [metadata/GlotScript.tsv](./metadata/GlotScript.tsv); see the [metadata folder](./metadata/) for its
format and sources.

## Citation
If you use any part of this our resource or tool in your research, please cite it using the following BibTex entry. 

```python
@inproceedings{kargaran-etal-2024-glotscript-resource,
    title = "{G}lot{S}cript: A Resource and Tool for Low Resource Writing System Identification",
    author = {Kargaran, Amir Hossein  and
      Yvon, Fran{\c{c}}ois  and
      Sch{\"u}tze, Hinrich},
    editor = "Calzolari, Nicoletta  and
      Kan, Min-Yen  and
      Hoste, Veronique  and
      Lenci, Alessandro  and
      Sakti, Sakriani  and
      Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.687",
    pages = "7774--7784"
}

```
