from .GlotScript import get_script_predictor
from .GlotScript import separate_script


sp = get_script_predictor(replace_punctuation=True, replace_digits=True)
sc = separate_script

__version__ = '1.2'
