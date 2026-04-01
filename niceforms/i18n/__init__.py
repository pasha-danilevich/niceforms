from pathlib import Path

from niceforms.i18n.translator import Translator

BASE_PATH = Path(__file__).parent / "locales"

tr = Translator(locale='ru', path=BASE_PATH)