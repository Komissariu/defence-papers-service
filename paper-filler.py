import re
from typing import Dict, Any, List, Callable


class PaperFiller:
    pattern = r'\{\{([a-z][a-zA-Z0-9_]*)\}\}'
    
    def __init__(self, template_number: int) -> None:
        self.template_number = template_number
        self.variables: List[str] = []
        self.template_content: str = ""
        self._load_template()
    
    def _load_template(self) -> None:
        try:
            with open(f"templates/{self.template_number}.txt", "r", encoding="UTF-8") as bytestream:
                self.template_content = bytestream.read()
                self.variables = re.findall(PaperFiller.pattern, self.template_content)
                self.variables = list(dict.fromkeys(self.variables))
        except FileNotFoundError:
            raise FileNotFoundError(f"Шаблон templates/{self.template_number}.txt не найден")
        except Exception as e:
            raise Exception(f"Ошибка при загрузке шаблона: {e}")
    
    def get_variables(self) -> List[str]:
        return self.variables.copy()
    
    def get_variable_count(self) -> int:
        return len(self.variables)
    
    def fill(self, values: Dict[str, Any], strict: bool = False) -> str:
        """
        Заполняет шаблон значениями из словаря.
        
        Args:
            values: Словарь с значениями для переменных
            strict: Если True, выбрасывает исключение при отсутствии значения для переменной
                   Если False, оставляет переменную как есть
        
        Returns:
            Заполненный текст
        """
        def replace_callback(match: re.Match) -> str:
            var_name = match.group(1)
            if var_name in values:
                return str(values[var_name])
            elif strict:
                raise KeyError(f"Не найдено значение для переменной: {var_name}")
            else:
                return match.group(0)  # Оставляем как есть
        
        try:
            return re.sub(PaperFiller.pattern, replace_callback, self.template_content)
        except KeyError as e:
            raise e
        except Exception as e:
            raise Exception(f"Ошибка при заполнении шаблона: {e}")
    
    def fill_with_function(self, func: Callable[[str], str]) -> str:
        """
        Заполняет шаблон с помощью пользовательской функции.
        
        Args:
            func: Функция, которая принимает имя переменной и возвращает строку
        
        Returns:
            Заполненный текст
        """
        def replace_callback(match: re.Match) -> str:
            var_name = match.group(1)
            return func(var_name)
        
        try:
            return re.sub(PaperFiller.pattern, replace_callback, self.template_content)
        except Exception as e:
            raise Exception(f"Ошибка при заполнении шаблона: {e}")
    
    def save_filled(self, output_path: str, values: Dict[str, Any], strict: bool = False) -> None:
        """
        Заполняет шаблон и сохраняет результат в файл.
        
        Args:
            output_path: Путь для сохранения результата
            values: Словарь с значениями для переменных
            strict: Если True, выбрасывает исключение при отсутствии значения для переменной
        """
        filled_content = self.fill(values, strict)
        try:
            with open(output_path, "w", encoding="UTF-8") as f:
                f.write(filled_content)
        except Exception as e:
            raise Exception(f"Ошибка при сохранении результата: {e}")
    
    def add_variable(self, var_name: str) -> None:
        """
        Добавляет переменную в список (для ручного управления).
        Проверяет, соответствует ли переменная паттерну.
        """
        if not re.match(r'^' + PaperFiller.pattern[2:-2] + r'$', var_name):
            raise ValueError(f"Некорректное имя переменной: {var_name}")
        if var_name not in self.variables:
            self.variables.append(var_name)
    
    def get_missing_variables(self, values: Dict[str, Any]) -> List[str]:
        return [var for var in self.variables if var not in values]
    
    def __str__(self) -> str:
        return f"PaperFiller(template={self.template_number}, variables={len(self.variables)})"
    
    def __repr__(self) -> str:
        return self.__str__()

