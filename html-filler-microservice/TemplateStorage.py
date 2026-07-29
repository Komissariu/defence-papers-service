from pathlib import Path

class TemplateStorage:
    def __init__(self, templates_dir: str = "templates", output_dir: str = "output") -> None:
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_template(self, template_name: str) -> str:
        file_path = self.templates_dir / f"{template_name}.txt"
        if not file_path.exists():
            raise FileNotFoundError(f"Шаблон '{file_path}' не найден.")
        return file_path.read_text(encoding="utf-8")

    def save_result(self, filename: str, content: str) -> Path:
        output_path = self.output_dir / filename
        output_path.write_text(content, encoding="utf-8")
        return output_path.resolve()
