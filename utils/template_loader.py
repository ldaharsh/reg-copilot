# utils/template_loader.py
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(default=False)  # ✅ Corrected
)

def render(name: str, **params) -> str:
    """
    Render a Jinja2 template by its *basename* (no extension).

    Example:
        text = render("cvb_summary", content="30 calves…")
    """
    tpl = env.get_template(f"{name}.j2")
    return tpl.render(**params)
