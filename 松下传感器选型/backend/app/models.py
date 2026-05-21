from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DetectionType(str, Enum):
    through_beam = "through_beam"
    retro_reflective = "retro_reflective"
    diffuse_reflective = "diffuse_reflective"
    distance_set = "distance_set"
    limited_reflective = "limited_reflective"
    auto = "auto"


class OutputType(str, Enum):
    npn = "npn"
    pnp = "pnp"
    any = "any"


class SelectionRequest(BaseModel):
    detection_type: DetectionType = DetectionType.auto
    detection_distance_mm: float = Field(
        ..., ge=1, description="所需检测距离（毫米）"
    )
    transparent_object: bool = False
    small_spot: bool = False
    narrow_beam: bool = False
    pcb_detection: bool = False
    oil_resistant: bool = False
    output_type: OutputType = OutputType.any
    top_n: int = Field(default=5, ge=1, le=20)


class ProductItem(BaseModel):
    model_base: str
    series: str
    detection_type: str
    detection_type_label: str
    detection_distance_mm: float
    detection_distance_text: str
    light_source: str
    features: list[str]
    output_npn: str
    output_pnp: str
    transparent_object: bool
    small_spot: bool
    narrow_beam: bool
    pcb_detection: bool
    needs_reflector: bool = False


class RecommendationItem(BaseModel):
    product: ProductItem
    recommended_model: str
    score: float
    reasons: list[str]


class SelectionResponse(BaseModel):
    requirements_summary: str
    recommendations: list[RecommendationItem]
    catalog_count: int


class CatalogResponse(BaseModel):
    items: list[ProductItem]
    source: str
    pdf_files: list[str]


class PdfImportResponse(BaseModel):
    message: str
    files_processed: list[str]
    models_found: int
    catalog_count: int
