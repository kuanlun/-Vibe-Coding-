import json
from pathlib import Path

from .models import ProductItem

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CATALOG_PATH = DATA_DIR / "catalog.json"
PDF_DIR = DATA_DIR / "pdfs"


def ensure_dirs() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)


def load_catalog() -> list[ProductItem]:
    ensure_dirs()
    if not CATALOG_PATH.exists():
        return []
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return [ProductItem.model_validate(item) for item in raw]


def save_catalog(items: list[ProductItem]) -> None:
    ensure_dirs()
    payload = [item.model_dump() for item in items]
    CATALOG_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def merge_catalog(existing: list[ProductItem], incoming: list[ProductItem]) -> list[ProductItem]:
    by_base = {p.model_base: p for p in existing}
    for product in incoming:
        by_base[product.model_base] = product
    return sorted(by_base.values(), key=lambda p: p.model_base)


def list_pdf_files() -> list[str]:
    ensure_dirs()
    return sorted(p.name for p in PDF_DIR.glob("*.pdf"))
