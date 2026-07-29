import re
from typing import Dict, Any, List

class TemplateRenderer:
    PATTERN = r'\{\{([a-z][a-zA-Z0-9_]*)\}\}'

    @classmethod
    def extract_variables(cls, content: str) -> List[str]:
        """Находит уникальные переменные в порядке их появления."""
        found = re.findall(cls.PATTERN, content)
        return list(dict.fromkeys(found))

    @classmethod
    def get_missing_variables(cls, content: str, values: Dict[str, Any]) -> List[str]:
        """Возвращает список переменных, которых нет в словаре values."""
        required = cls.extract_variables(content)
        return [var for var in required if var not in values]

    @classmethod
    def render(cls, content: str, values: Dict[str, Any], strict: bool = False) -> str:
        """Подставляет значения в текст шаблона."""
        def replace_callback(match: re.Match) -> str:
            var_name = match.group(1)
            if var_name in values:
                return str(values[var_name])
            if strict:
                raise KeyError(f"Не найдено значение для переменной: '{var_name}'")
            return match.group(0)

        return re.sub(cls.PATTERN, replace_callback, content)
