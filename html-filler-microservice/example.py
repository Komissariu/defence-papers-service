from TemplateStorage import TemplateStorage
from DocumentService import DocumentService

# Инициализация (на старте сервиса)
storage = TemplateStorage(templates_dir="./templates", output_dir="./tmp/compiled_html")
doc_service = DocumentService(storage=storage)

# Обработка запроса
def handle_generate_pdf_request(payload: dict):
    # payload: {"template_id": "invoice_12", "data": {"user_name": "Ivan"}, "output_name": "doc_123.html"}
    
    saved_path = doc_service.process_document(
        template_id=payload["template_id"],
        values=payload["data"],
        output_filename=payload["output_name"],
        strict=True
    )
    
    # saved_path -> PosixPath('/app/tmp/compiled_html/doc_123.html')
    # Далее отдаем этот путь компилятору PDF/DOCX
    return str(saved_path)
