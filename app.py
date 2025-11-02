import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import requests
import hashlib
from io import BytesIO

# ============ CONFIG ============
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-1-5"
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]  # Add your Hugging Face token in Streamlit secrets

CACHE_DIR = "hf_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ====== UTILS ======
def load_font(font_name="arial.ttf", size=32):
    try:
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

def hash_prompt(prompt):
    return hashlib.md5(prompt.encode()).hexdigest()

def generate_sd_image(prompt):
    """
    Generate image via Hugging Face Stable Diffusion API with caching
    """
    # Check cache first
    prompt_hash = hash_prompt(prompt)
    cache_path = os.path.join(CACHE_DIR, f"{prompt_hash}.png")
    if os.path.exists(cache_path):
        return Image.open(cache_path)
    
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt}
    
    with st.spinner("Generating AI image..."):
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(cache_path)
            return image
        else:
            st.error(f"Error from Hugging Face API: {response.status_code}")
            return None

def overlay_text(image, business_type, headline, phone_number):
    """
    Overlay business info on AI-generated image
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Headline
    font_h = load_font(size=48)
    draw.text((width//2, 50), headline, font=font_h, fill="white", anchor="ms")
    
    # Business type badge
    font_b = load_font(size=36)
    draw.text((width//2, 120), f"{business_type.upper()} SERVICES", font=font_b, fill="yellow", anchor="ms")
    
    # Phone number at bottom
    font_p = load_font(size=32)
    draw.text((width//2, height-60), f"📞 {phone_number}", font=font_p, fill="white", anchor="ms")
    
    return image

# ======= STREAMLIT APP =======
st.set_page_config(page_title="Social Media Generator Pro", layout="wide")

st.title("🎯 Social Media Graphics Generator")
st.subheader("Generate professional posts instantly!")

# Sidebar
st.sidebar.header("💰 Plans")
st.sidebar.write("**Free:** 10 graphics/month")
st.sidebar.write("**Pro:** Unlimited + AI Content")
st.sidebar.write("Email: hello.contentos@gmail.com")

# Main content
business_type = st.selectbox("Business Type:", ["Plumbing", "Cleaning", "Landscaping", "HVAC", "Electrical"])
phone_number = st.text_input("Phone Number", value="(555) 123-4567")
headline = st.text_input("Headline", value=f"Professional {business_type} Services")
description = st.text_area("Description", value=f"Expert {business_type} solutions for your home or business. Quality work guaranteed!")

generate_option = st.radio("Image Type:", ["Free Template", "AI Generated (Pro)"])

if st.button("Generate Graphic", key="generate_graphic_btn"):
    if generate_option == "Free Template":
        # Use pre-generated placeholder template
        width, height = 800, 800
        image = Image.new("RGB", (width, height), color=(200, 200, 200))
        draw = ImageDraw.Draw(image)
        font_h = load_font(size=48)
        draw.text((width//2, height//2), "FREE TEMPLATE", font=font_h, fill=(50,50,50), anchor="mm")
    else:
        # AI generated via Hugging Face SD API
        prompt = f"{business_type} business social media post, professional, modern style"
        image = generate_sd_image(prompt)
        if image is None:
            st.error("Failed to generate AI image.")
            st.stop()
    
    # Overlay user text info
    image = overlay_text(image, business_type, headline, phone_number)
    
    # Display and download
    st.image(image, use_column_width=True)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    st.download_button("📥 Download Graphic", data=buffered.getvalue(), file_name=f"{business_type}_post.png", mime="image/png")
