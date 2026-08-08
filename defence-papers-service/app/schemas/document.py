from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentGenerateRequest(BaseModel):
    template_id: Optional[str] = Field(
        default=None,
        description="Идентификатор шаблона или название документа",
        example="candidate_dissertation_v1",
    )
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Свободная структура JSON, переданная с фронтенда",
        example={"candidate_name": "Иванов И.И.", "degree": "кандидат"},
    )


class DocumentGenerateResponse(BaseModel):
    file_path: str = Field(..., description="Путь к обработанному документу")
    status: str = Field(default="success", description="Статус генерации")


class VariableExtractionResponse(BaseModel):
    variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Нормализованный словарь переменных из входного JSON",
    )
    variable_names: List[str] = Field(
        default_factory=list,
        description="Список доступных имён переменных в порядке обхода JSON",
    )
    count: int = Field(default=0, description="Количество извлечённых переменных")


class VariableExtractionRequest(BaseModel):
    payload: Any = Field(
        ...,
        description="Произвольный JSON-фрейм, который прилетел с фронтенда",
    )
