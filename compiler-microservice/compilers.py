from abc import ABC, abstractmethod
import io
from pathlib import Path
from typing import Dict, Type

from docx import Document
from htmldocx import HtmlToDocx
from weasyprint import HTML


# 1. Ответственность: Безопасное чтение и валидация исходного файла
class DocumentReader:
    @staticmethod
    def read_html(path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"HTML файл не найден по пути: {path}")
        if not path.is_file():
            raise ValueError(f"Указанный путь не является файлом: {path}")
        return path.read_text(encoding="utf-8")


# 2. Ответственность: Общий интерфейс для конвертеров (OCP & DIP)
class BaseConverter(ABC):
    @abstractmethod
    def convert(self, file_path: Path) -> io.BytesIO:
        """Принимает путь к файлу и возвращает байтовый поток с итоговым документом."""
        pass


# 3. Ответственность: Конвертация HTML -> PDF
class PdfConverter(BaseConverter):
    def convert(self, file_path: Path) -> io.BytesIO:
        stream = io.BytesIO()
        # WeasyPrint сама загрузит относительные ресурсы (картинки, CSS), зная путь к файлу
        HTML(filename=str(file_path)).write_pdf(target=stream)
        stream.seek(0)
        return stream


# 4. Ответственность: Конвертация HTML -> DOCX
class DocxConverter(BaseConverter):
    def __init__(self, reader: DocumentReader = DocumentReader()):
        self._reader = reader

    def convert(self, file_path: Path) -> io.BytesIO:
        html_content = self._reader.read_html(file_path)
        
        doc = Document()
        parser = HtmlToDocx()
        parser.add_html_to_document(html_content, doc)

        stream = io.BytesIO()
        doc.save(stream)
        stream.seek(0)
        return stream


# 5. Ответственность: Оркестрация процесса и регистрация поддерживаемых форматов
class DocumentConversionService:
    def __init__(self):
        # Маппинг форматов к соответствующим конвертерам
        self._converters: Dict[str, Type[BaseConverter]] = {
            "pdf": PdfConverter,
            "docx": DocxConverter,
        }

    def register_converter(self, fmt: str, converter_cls: Type[BaseConverter]) -> None:
        """Позволяет легко расширять систему новыми форматами снаружи."""
        self._converters[fmt.lower()] = converter_cls

    def convert(self, html_path: str | Path, output_format: str) -> io.BytesIO:
        path = Path(html_path)
        fmt = output_format.lower()

        converter_cls = self._converters.get(fmt)
        if not converter_cls:
            supported = ", ".join(self._converters.keys())
            raise ValueError(
                f"Неподдерживаемый формат '{output_format}'. Доступные форматы: {supported}"
            )

        converter = converter_cls()
        return converter.convert(path)
