import json
import logging
from pathlib import Path
from typing import Optional, Union, TypeAlias

logger = logging.getLogger(__name__)


Locale: TypeAlias = str

class Translator:

    def __init__(
        self,
        locale: Locale,
        path: Path,
    ):
        self.locale = locale
        self.path = path

        self.messages = self._load(locale)

    def _load(self, locale: str) -> dict:
        with open(self.path / f"{locale}.json", encoding="utf-8") as f:
            return json.load(f)

    def add_custom_translations(self, translations: dict[str, str]):
        """Загрузка кастомных переводов из словаря"""
        # Глубокое слияние словарей
        self.messages = self._deep_merge(self.messages, translations)
        logger.info(f"Loaded {len(translations)} custom translations for: {self.locale}")


    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Глубокое слияние словарей"""
        result = base.copy()
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

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
