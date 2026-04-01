import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, locale: str, path: Path):
        self.locale = locale
        self.path = path
        self.messages = self._load(locale)

    def _load(self, locale: str) -> dict:
        with open(self.path / f"{locale}.json", encoding="utf-8") as f:
            return json.load(f)

    def translate(
        self,
        code: str,
        ctx: Optional[dict] = None,
        default: Optional[str] = 'Error translation',
    ) -> str:
        template = self.messages.get(code)
        if not template:
            logger.warning(f"No translation for <{code=}> <{ctx=}>")
            return default
        if ctx:
            return template.format(**ctx)
        return template
