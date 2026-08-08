from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException

from app.schemas.document import (
    DocumentGenerateRequest,
    DocumentGenerateResponse,
    VariableExtractionResponse,
)

api_router = APIRouter()


def flatten_payload(payload: Any, prefix: str = "") -> Dict[str, Any]:
    """
    Рекурсивно разворачивает JSON-фрейм в flat-словарь, доступный для последующей
    сборки документа. Так frontend сможет послать произвольную структуру, а сервер
    спокойно извлечёт имена полей (variables) без жёсткой схемы.
    """
    flat: Dict[str, Any] = {}

    if isinstance(payload, dict):
        for key, value in payload.items():
            key_name = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, (dict, list)):
                flat.update(flatten_payload(value, key_name))
            else:
                flat[key_name] = value

    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            key_name = f"{prefix}[{index}]" if prefix else f"[{index}]"
            if isinstance(value, (dict, list)):
                flat.update(flatten_payload(value, key_name))
            else:
                flat[key_name] = value

    else:
        if prefix:
            flat[prefix] = payload
        else:
            flat["root"] = payload

    return flat


@api_router.post(
    "/documents/extract-variables",
    response_model=VariableExtractionResponse,
    summary="Извлекает словарь переменных из свободного JSON от фронтенда",
)
def extract_variables(payload: Any = Body(...)) -> VariableExtractionResponse:
    """
    Принимает тело запроса любого JSON-типа: объект, массив, число, строку.
    Возвращает flat-представление данных, чтобы фронтенд мог передать их в генератор
    шаблонов. Типичный кейс — payload = {"candidate": {...}, "thesis": {...}}.
    """
    if payload is None:
        raise HTTPException(status_code=400, detail="JSON body is required")

    variables = flatten_payload(payload)
    variable_names = list(variables.keys())

    return VariableExtractionResponse(
        variables=variables,
        variable_names=variable_names,
        count=len(variable_names),
    )


@api_router.post(
    "/documents/generate",
    response_model=DocumentGenerateResponse,
    summary="Легкая заглушка для генерации документа",
)
def generate_document(request: DocumentGenerateRequest) -> DocumentGenerateResponse:
    """
    Первичный контракт: принимает идентификатор шаблона и JSON-данные.
    На текущем этапе отвечает только сообщением о принятии и готовит место для
    дальнейшего вызова микросервисов.
    """
    return DocumentGenerateResponse(
        file_path=f"/tmp/generated/{request.template_id or 'candidate_dissertation'}.html",
        status="accepted",
    )
