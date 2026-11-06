from .GlotScript import get_script_predictor
from .GlotScript import separate_script
from .GlotScript import script_segments
from .GlotScript import word_scripts
from .GlotScript import script_covers, COMPOSITE_SCRIPTS
from .ranges import SCRIPT_RANGES, UNICODE_VERSION


sp = get_script_predictor(replace_punctuation=True, replace_digits=True)
sc = separate_script
ss = script_segments
ws = word_scripts

__version__ = '2.1'
