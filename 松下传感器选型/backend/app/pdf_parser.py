import re
from pathlib import Path

import pdfplumber

from .catalog import PDF_DIR, load_catalog, merge_catalog, save_catalog
from .models import ProductItem

# 从 PDF 文本中匹配「检测距离 + 型号」行，用于补充/更新目录
CATALOG_LINE = re.compile(
    r"(?P<dist>\d+(?:\.\d+)?)\s*(?:m|mm|米|毫米)?\s+"
    r"(?P<model>CX-4\d{2})(?:\s+(?P<model_p>CX-4\d{2}-P))?",
    re.IGNORECASE,
)

TYPE_KEYWORDS: list[tuple[str, str, str]] = [
    ("透过", "through_beam", "透过型"),
    ("回归反射", "retro_reflective", "回归反射型"),
    ("扩散反射", "diffuse_reflective", "扩散反射型"),
    ("距离设定", "distance_set", "距离设定反射型"),
    ("限定反射", "limited_reflective", "限定反射型"),
    ("透明", "retro_reflective", "回归反射型（透明体）"),
]


def _distance_to_mm(value: float, unit_hint: str) -> float:
    if "m" in unit_hint.lower() and "mm" not in unit_hint.lower():
        if value < 50:
            return value * 1000
    return value


def _guess_type(text: str) -> tuple[str, str]:
    for keyword, dtype, label in TYPE_KEYWORDS:
        if keyword in text:
            return dtype, label
    return "diffuse_reflective", "扩散反射型"


def extract_products_from_text(text: str) -> list[ProductItem]:
    products: dict[str, ProductItem] = {}
    context_window = ""
    for line in text.splitlines():
        context_window = (context_window + "\n" + line)[-500:]
        for match in CATALOG_LINE.finditer(line):
            model = match.group("model").upper()
            if not model.startswith("CX-4"):
                continue
            dist_raw = float(match.group("dist"))
            unit_hint = line
            dist_mm = _distance_to_mm(dist_raw, unit_hint)
            dtype, dlabel = _guess_type(context_window)
            npn = model
            pnp = match.group("model_p") or f"{model}-P"
            products[model] = ProductItem(
                model_base=model,
                series="CX-400",
                detection_type=dtype,
                detection_type_label=dlabel,
                detection_distance_mm=dist_mm,
                detection_distance_text=line.strip()[:80],
                light_source="红色LED",
                features=["从本地 PDF 解析"],
                output_npn=npn.upper(),
                output_pnp=pnp.upper(),
                transparent_object="透明" in context_window,
                small_spot="小光点" in context_window or "φ2" in context_window,
                narrow_beam="窄视角" in context_window,
                pcb_detection="基板" in context_window or "SMT" in context_window,
                needs_reflector=dtype == "retro_reflective",
            )
    return list(products.values())


def parse_pdf_file(path: Path) -> list[ProductItem]:
    text_parts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return extract_products_from_text("\n".join(text_parts))


def import_all_pdfs() -> tuple[list[str], int]:
    from .catalog import ensure_dirs

    ensure_dirs()
    processed: list[str] = []
    found: list[ProductItem] = []
    for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
        processed.append(pdf_path.name)
        found.extend(parse_pdf_file(pdf_path))
    if found:
        merged = merge_catalog(load_catalog(), found)
        save_catalog(merged)
    return processed, len(found)
