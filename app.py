# app.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import json
import requests
from datetime import datetime

# ================= CONFIG ==================
st.set_page_config(page_title="Social Media Generator Pro", page_icon="🎯", layout="wide")

CACHE_DIR = "hf_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ================ SECRETS ==================
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN")
if HF_API_TOKEN is None:
    st.error("Hugging Face API token not found in Streamlit secrets!")
    st.stop()

HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# ================ HELPER FUNCTIONS ==================
def load_font(font_name, size):
    try:
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

def create_template_modern(business_type, headline, description, phone_number, colors):
    width, height = 800, 800
    image = Image.new('RGB', (width, height), color=(255,255,255))
    draw = ImageDraw.Draw(image)

    # Gradient background
    for i in range(height):
        r = int(colors["primary"][0]*(1-i/height) + 230*(i/height))
        g = int(colors["primary"][1]*(1-i/height) + 230*(i/height))
        b = int(colors["primary"][2]*(1-i/height) + 230*(i/height))
        draw.line([(0,i),(width,i)], fill=(r,g,b))

    headline_font = load_font("arial.ttf", 48)
    wrapped_headline = textwrap.fill(headline, width=20)
    draw.text((width//2,100), wrapped_headline, fill=(0,0,0), anchor="mm", align="center")

    badge_font = load_font("arial.ttf", 36)
    badge_text = f"{business_type.upper()} SERVICES"
    draw.text((width//2,200), badge_text, fill=colors["primary"], font=badge_font, anchor="mm")

    desc_font = load_font("arial.ttf", 28)
    wrapped_desc = textwrap.fill(description, width=30)
    draw.multiline_text((width//2,400), wrapped_desc, fill=(50,50,50), font=desc_font, anchor="mm", align="center")

    phone_font = load_font("arial.ttf", 32)
    draw.text((width//2,height-100), f"📞 {phone_number}", fill=colors["accent"], font=phone_font, anchor="mm")

    return image

def call_hf_sd(prompt: str):
    """Call Hugging Face SD API and return PIL image"""
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=HEADERS, json=payload, stream=True)
    if response.status_code != 200:
        st.error(f"Hugging Face API error: {response.status_code}")
        return None
    image = Image.open(response.raw).convert("RGB")
    return image

def create_social_media_graphic(template_type, business_type, headline, description, phone_number, use_ai=False):
    colors = {
        "Plumbing": {"primary": (0,90,180), "accent": (255,140,0)},
        "Cleaning": {"primary": (30,110,40), "accent": (255,193,7)},
        "Landscaping": {"primary": (40,120,45), "accent": (255,167,38)},
        "HVAC": {"primary": (180,30,30), "accent": (66,133,244)},
        "Electrical": {"primary": (110,25,140), "accent": (255,214,0)}
    }.get(business_type, {"primary": (0,90,180), "accent": (255,140,0)})

    if use_ai:
        prompt = f"A professional social media graphic for a {business_type} business: {headline}, {description}"
        image = call_hf_sd(prompt)
        if image is None:
            return create_template_modern(business_type, headline, description, phone_number, colors)
        return image
    else:
        return create_template_modern(business_type, headline, description, phone_number, colors)

# ================= SIDEBAR ==================
with st.sidebar:
    st.header("💰 Pricing")
    st.write("**Free:** 10 graphics/month (templates only)")
    st.write("**Pro ($29/month):** Unlimited + AI Content")
    st.header("💳 Upgrade Now")
    if st.button("Start $29/month Pro Plan"):
        st.success("Pro plan selected! Contact: hello.contentos@gmail.com")
    st.header("💡 Need Help?")
    st.write("Email: hello.contentos@gmail.com")

# ================= MAIN ==================
st.title("🎨 Social Media Generator Pro")

tab1, tab2 = st.tabs(["Create Graphics", "Content Ideas"])

with tab1:
    business_type = st.selectbox("Business Type:", ["Plumbing", "Cleaning", "Landscaping", "HVAC", "Electrical"])
    template_type = st.selectbox("Design Template:", ["Modern Professional"])
    phone_number = st.text_input("Phone Number", "(555) 123-4567")
    headline = st.text_input("Headline", f"Professional {business_type} Services")
    description = st.text_area("Description", f"Expert {business_type} solutions for your home or business. Quality work guaranteed! Contact us today.")
    use_ai = st.checkbox("Use AI-generated background (Pro)", value=False)

    if st.button("Generate Graphic"):
        with st.spinner("Creating your professional graphic..."):
            image = create_social_media_graphic(template_type, business_type, headline, description, phone_number, use_ai)
            image_path = f"output/graphic_{datetime.now().strftime('%H%M%S')}.png"
            os.makedirs("output", exist_ok=True)
            image.save(image_path)
            st.image(image_path, use_container_width=True)
            with open(image_path, "rb") as file:
                st.download_button("📥 Download Graphic", data=file, file_name=f"{business_type}_post.png", mime="image/png")

with tab2:
    st.header("30-Day Content Ideas")
    content_ideas = [
        "Monday: Service highlight",
        "Tuesday: Customer testimonial",
        "Wednesday: Educational tip",
        "Thursday: Before/after transformation",
        "Friday: Weekend special offer",
        "Saturday: Team spotlight",
        "Sunday: Industry news"
    ]
    for idea in content_ideas:
        st.write(f"✅ {idea}")
    st.download_button("📥 Download Content Calendar", data=json.dumps(content_ideas, indent=2), file_name="content_calendar.json", mime="application/json")
