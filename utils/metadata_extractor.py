"""Извлечение метаданных из FieldInfo."""

from pydantic.fields import FieldInfo


class MetadataExtractor:
    """Извлекает метаданные из FieldInfo."""

    @staticmethod
    def extract(field_info: FieldInfo) -> dict[str, str]:
        return {
            "label": field_info.title or "",
            "description": field_info.description or "",
        }
