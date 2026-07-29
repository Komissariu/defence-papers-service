from typing import Dict, Any
from pathlib import Path

from TemplateStorage import TemplateStorage
from TemplateRenderer import TemplateRenderer

class DocumentService:
    def __init__(self, storage: TemplateStorage, renderer: type[TemplateRenderer] = TemplateRenderer) -> None:
        self.storage = storage
        self.renderer = renderer

    def process_document(
        self, 
        template_id: str, 
        values: Dict[str, Any], 
        output_filename: str, 
        strict: bool = True
    ) -> Path:
        """
        Основной метод сервиса:
        Принимает имя шаблона и данные -> отдаёт путь к готовому файлу.
        """
        # 1. Загружаем шаблон
        content = self.storage.load_template(template_id)
        
        # 2. Рендерим
        rendered_content = self.renderer.render(content, values, strict=strict)
        
        # 3. Сохраняем и возвращаем полный путь к файлу
        return self.storage.save_result(output_filename, rendered_content)
