import streamlit as st
import requests

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

st.set_page_config(page_title="🎨 CORTEX Prompt Generator", layout="centered")

st.title("🧠🎨 CORTEX Prompt Generator")
st.markdown("یک ابزار برای تولید پرامپت‌های تصویری حرفه‌ای برای مدل‌هایی مثل Midjourney و DALL·E")

# ورودی کاربر
base_topic = st.text_input("🔹 موضوع اصلی تصویر", "a robot playing violin")
style = st.text_input("🎨 سبک هنری (مثلاً cyberpunk, watercolor, realism)", "steampunk")
emotion = st.text_input("❤️ احساس غالب تصویر", "melancholic")
camera_angle = st.text_input("🎥 زاویه دوربین", "side view")
purpose = st.text_input("🎯 هدف تصویر (مثلاً concept art, game asset)", "concept art")
context_layers = st.text_input("🌍 عناصر زمینه (با کاما جدا کن)", "foggy, industrial, night")
weird = st.slider("🌀 درجه عجیب بودن تصویر", 0.0, 1.0, 0.5)
chaos = st.slider("🔥 میزان بی‌نظمی یا آشوب", 0.0, 1.0, 0.5)
detail_level = st.selectbox("🧩 سطح جزئیات", ["low", "medium", "high"])
apply_scamper = st.checkbox("✨ خلاقیت (SCAMPER)", value=True)
language = st.radio("🌐 زبان خروجی", ["en", "fa"])

# ورودی Webhook URL دیسکورد
webhook_url = st.text_input("🌐 Webhook URL دیسکورد (اختیاری برای ارسال مستقیم)")

if st.button("✅ تولید و ارسال پرامپت"):
    prompt = CORTEX_generate(
        base_topic=base_topic,
        style=style,
        emotion=emotion,
        camera_angle=camera_angle,
        purpose=purpose,
        context_layers=[c.strip() for c in context_layers.split(",") if c.strip()],
        weird=weird,
        chaos=chaos,
        detail_level=detail_level,
        apply_scamper=apply_scamper,
        language=language
    )
    st.success("🎉 پرامپت شما آماده‌ست:")
    st.code(prompt, language="text")

    # ارسال پرامپت به Discord در صورت وارد شدن webhook_url
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"content": prompt})
            if response.status_code == 204:
                st.success("🚀 پرامپت با موفقیت به دیسکورد ارسال شد!")
            else:
                st.error(f"❌ ارسال ناموفق بود. کد پاسخ: {response.status_code}")
        except Exception as e:
            st.error(f"❌ خطا در ارسال به دیسکورد: {e}")
