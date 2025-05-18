def CORTEX_generate(
    base_topic: str,
    style: str = None,
    emotion: str = None,
    camera_angle: str = None,
    purpose: str = None,
    weird: float = 0.5,
    chaos: float = 0.5,
    detail_level: str = "medium",
    context_layers: list = None,
    apply_scamper: bool = True,
    language: str = "en"
) -> str:
    parts = []

    if emotion:
        parts.append(f"{emotion}")
    if style:
        parts.append(f"{style}")
    parts.append(base_topic)
    if camera_angle:
        parts.append(f"seen from {camera_angle}")
    if context_layers:
        parts.append(", ".join(context_layers))
    if detail_level:
        parts.append(f"{detail_level} detail")
    if apply_scamper:
        parts.append("with imaginative twists and visual metaphors")
    parts.append(f"weirdness level: {weird}")
    parts.append(f"chaotic elements: {chaos}")
    if purpose:
        parts.append(f"intended for {purpose}")

    prompt = ", ".join(parts)

    if language == "fa":
        prompt = "پرامپت تصویری: " + prompt.replace("seen from", "از زاویهٔ").replace("detail", "جزئیات")

    return prompt
