from .models import (
    DetectionType,
    OutputType,
    ProductItem,
    RecommendationItem,
    SelectionRequest,
)


DETECTION_TYPE_LABELS = {
    "through_beam": "透过型",
    "retro_reflective": "回归反射型",
    "diffuse_reflective": "扩散反射型",
    "distance_set": "距离设定反射型",
    "limited_reflective": "限定反射型",
}


def _pick_model(product: ProductItem, output: OutputType) -> str:
    if output == OutputType.pnp:
        return product.output_pnp
    if output == OutputType.npn:
        return product.output_npn
    return product.output_npn


def _score_product(req: SelectionRequest, product: ProductItem) -> tuple[float, list[str]]:
    score = 100.0
    reasons: list[str] = []

    if req.detection_type != DetectionType.auto:
        if product.detection_type != req.detection_type.value:
            score -= 45
            reasons.append(
                f"检测方式不完全匹配（需求：{DETECTION_TYPE_LABELS.get(req.detection_type.value, req.detection_type.value)}）"
            )
        else:
            reasons.append("检测方式匹配")
            score += 8

    dist = product.detection_distance_mm
    req_dist = req.detection_distance_mm
    if dist >= req_dist:
        margin = (dist - req_dist) / max(req_dist, 1)
        if margin <= 0.5:
            score += 15
            reasons.append(f"检测距离 {product.detection_distance_text} 满足需求且余量适中")
        else:
            score += 5
            reasons.append(f"检测距离满足需求，余量较大（{product.detection_distance_text}）")
    else:
        gap = (req_dist - dist) / max(req_dist, 1)
        penalty = min(50, 20 + gap * 40)
        score -= penalty
        reasons.append(
            f"标称检测距离可能不足（需求约 {int(req_dist)}mm，型号 {product.detection_distance_text}）"
        )

    if req.transparent_object:
        if product.transparent_object:
            score += 20
            reasons.append("支持透明物体检测")
        else:
            score -= 35
            reasons.append("非透明体专用型，透明检测可能不稳定")

    if req.small_spot and product.small_spot:
        score += 12
        reasons.append("具备小光点/高精度特性")

    if req.narrow_beam and product.narrow_beam:
        score += 10
        reasons.append("窄视角型，适合狭长检测区域")

    if req.pcb_detection and product.pcb_detection:
        score += 18
        reasons.append("适合 PCB / 基板检测")

    if req.oil_resistant:
        oil_ok = any("抗油" in f or "IP67" in f for f in product.features)
        if oil_ok:
            score += 8
            reasons.append("具备耐环境（抗油/IP67）特性")
        else:
            score -= 5

    if req.detection_type == DetectionType.auto and not reasons:
        reasons.append("综合距离与特殊需求评分")

    return max(0.0, score), reasons


def recommend(
    catalog: list[ProductItem], req: SelectionRequest
) -> list[RecommendationItem]:
    scored: list[RecommendationItem] = []
    for product in catalog:
        score, reasons = _score_product(req, product)
        scored.append(
            RecommendationItem(
                product=product,
                recommended_model=_pick_model(product, req.output_type),
                score=round(score, 1),
                reasons=reasons,
            )
        )
    scored.sort(key=lambda x: x.score, reverse=True)
    return scored[: req.top_n]


def summarize_requirements(req: SelectionRequest) -> str:
    parts = [f"检测距离 ≥ {int(req.detection_distance_mm)} mm"]
    if req.detection_type != DetectionType.auto:
        parts.append(DETECTION_TYPE_LABELS.get(req.detection_type.value, req.detection_type.value))
    if req.transparent_object:
        parts.append("透明物体")
    if req.small_spot:
        parts.append("小光点/细小工件")
    if req.narrow_beam:
        parts.append("窄视角")
    if req.pcb_detection:
        parts.append("PCB基板")
    if req.oil_resistant:
        parts.append("耐油/IP67环境")
    if req.output_type != OutputType.any:
        parts.append(f"输出：{req.output_type.value.upper()}")
    return "；".join(parts)
