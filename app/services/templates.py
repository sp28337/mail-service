from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


class TemplateRenderer:
    def __init__(self, directory: str) -> None:
        self._env = Environment(
            loader=FileSystemLoader(directory),
            autoescape=select_autoescape(["html", "xml"]),
            undefined=StrictUndefined,
        )

    def render(self, template_name: str, context: dict[str, str]) -> str:
        template = self._env.get_template(template_name)
        return template.render(**context)
