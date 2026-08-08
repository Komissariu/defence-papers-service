Komissar 2026-08-08 работал с main-service
1. В gitignore добавлены чувствительные вещи (venv и пока что закоментированный .env)
2. Начат reqirements.txt
3. Сформирован config.py, который хавает данные с .env
4. Думаю полезно начать вести чейнджлог, чтобы лучше понимать что происходит и отслеживать работу
5. Сделан черновик main.py
6. На уровне main-service введён абстрактный POST-контракт для свободного JSON: /api/v1/documents/extract-variables. Он принимает любой JSON-объект/массив/значение, разворачивает его в flat-переменные (например, candidate.name, thesis_title, reviewers[0]) и возвращает response_model с variables, variable_names и count.
7. Проверка прошла через проектный venv-интерпретатор: POST on /api/v1/documents/extract-variables получил HTTP 200 и вернул плоский словарь переменных с 4 полями на тестовом payload.
8. Обнаружена и исправлена опечатка в settings-поле PROJECT_NAME, блокировавшая создание FastAPI-приложения на старте; теперь конфиг читает имя проекта корректно.