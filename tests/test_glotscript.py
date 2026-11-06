"""Tests of GlotScript: python tests/test_glotscript.py (or pytest tests)."""
import os
import string
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from GlotScript import (get_script_predictor, script_covers, script_segments, separate_script,  # noqa: E402
                        word_scripts)
from GlotScript.GlotScript import _char_scripts  # noqa: E402


def test_predict_script():
    predictor_fn = get_script_predictor()

    assert predictor_fn("this is a latin script.")[:2] == ("Latn", 1.0)
    assert predictor_fn("isso é escrita latina 1234")[:2] == ("Latn", 1.0)
    assert predictor_fn("এটি বাংলা লিপি")[:2] == ("Beng", 1.0)
    assert predictor_fn("นี่คืออักษรไทย")[:2] == ("Thai", 1.0)
    assert predictor_fn("자미로콰이 Jamiroquai는 영국의 애시드 재즈 밴드이다 자미로콰이는 년대 초반 런던에서 활발하게 일어난 애시드 재즈")[:2] == ("Hang", 0.8148148148148148)
    assert predictor_fn("이어지는기사  에서그점  에관해알려줄것  입니다")[:2] == ("Hang", 1.0)

    # empty
    assert predictor_fn(string.digits)[:2] == (None, 0)
    assert predictor_fn(string.whitespace)[:2] == (None, 0)
    assert predictor_fn("")[:2] == (None, 0)


def test_separate_script():

    sent = "Hello Salut سلام 你好 こんにちは שלום مرحبا"
    detected_scripts = separate_script(sent)

    ground_truth = {
        'Latn': 'Hello Salut     ',
        'Hebr': '     שלום ',
        'Arab': '  سلام    مرحبا',
        'Hani': '   你好   ',
        'Hira': '    こんにちは  '
    }

    for key in ground_truth.keys():
        assert key in detected_scripts, f"Error: '{key}' script not found in detected scripts."
        
        detected_tokens = [x.strip() for x in detected_scripts[key].split() if len(x.strip()) != 0]
        ground_truth_tokens = [x.strip() for x in ground_truth[key].split() if len(x.strip()) != 0]

        assert sorted(detected_tokens) == sorted(ground_truth_tokens), f"Error: Tokens for key '{key}' do not match."


def test_replacement_character():
    assert _char_scripts("�") == ('Zzzz',)
    assert get_script_predictor()("��")[:2] == ("Zzzz", 1.0)


def test_script_segments():
    text = "Hello Salut سلام 你好"
    segs = script_segments(text)
    assert segs == [('Latn', 0, 11, 'Hello Salut'), ('Zyyy', 11, 12, ' '), ('Arab', 12, 16, 'سلام'),
                    ('Zyyy', 16, 17, ' '), ('Hani', 17, 19, '你好')]
    assert "".join(s[3] for s in segs) == text and all(text[a:b] == t for _, a, b, t in segs)
    # common characters between segments of the same script join them; combining marks stay with their letter
    assert script_segments("नमस्ते दुनिया, hello") == [('Deva', 0, 13, 'नमस्ते दुनिया'), ('Zyyy', 13, 15, ', '),
                                                     ('Latn', 15, 20, 'hello')]
    assert script_segments("é a") == [('Latn', 0, 4, 'é a')]
    assert script_segments("I love 你好", common="separate") == [('Latn', 0, 1, 'I'), ('Zyyy', 1, 2, ' '),
                                                                 ('Latn', 2, 6, 'love'), ('Zyyy', 6, 7, ' '),
                                                                 ('Hani', 7, 9, '你好')]
    assert script_segments("") == [] and script_segments("2024!") == [('Zyyy', 0, 5, '2024!')]


def test_script_covers():
    assert script_covers('Jpan', 'Hira') and script_covers('Jpan', 'Hani') and script_covers('Kore', 'Hang')
    assert script_covers('Hant', 'Hani') and script_covers('Latn', 'Latn')
    assert not script_covers('Latn', 'Cyrl') and not script_covers('Hani', 'Hira')


def test_word_scripts():
    assert word_scripts("I love 你好, ok!") == [('I', 'Latn'), ('love', 'Latn'), ('你好,', 'Hani'), ('ok!', 'Latn')]
    assert word_scripts("Привет, world. 2024") == [('Привет,', 'Cyrl'), ('world.', 'Latn'), ('2024', 'Zyyy')]
    assert word_scripts("   ") == []


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
