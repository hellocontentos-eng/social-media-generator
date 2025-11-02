import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import json
from datetime import datetime, timedelta
import replicate
import requests
import time
from io import BytesIO

replicate_client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

# App configuration
st.set_page_config(
    page_title="Social Media Generator Pro",
    page_icon="🎯",
    layout="wide"
)

import replicate
import time

# Configure Replicate
replicate_client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

# PRE-GENERATED BACKGROUND CACHE (generate these once, use forever)
BACKGROUND_CACHE = {
    "Plumbing": [
        "https://replicate.delivery/pbxt/ABC123/plumbing_bg1.png",  # Will replace with actual generated URLs
        "https://replicate.delivery/pbxt/ABC124/plumbing_bg2.png",
        "https://replicate.delivery/pbxt/ABC125/plumbing_bg3.png",
        "https://replicate.delivery/pbxt/ABC126/plumbing_bg4.png",
        "https://replicate.delivery/pbxt/ABC127/plumbing_bg5.png"
    ],
    "Cleaning": [
        "https://replicate.delivery/pbxt/DEF123/cleaning_bg1.png",
        "https://replicate.delivery/pbxt/DEF124/cleaning_bg2.png",
        "https://replicate.delivery/pbxt/DEF125/cleaning_bg3.png",
        "https://replicate.delivery/pbxt/DEF126/cleaning_bg4.png",
        "https://replicate.delivery/pbxt/DEF127/cleaning_bg5.png"
    ],
    "HVAC": [
        "https://replicate.delivery/pbxt/GHI123/hvac_bg1.png",
        "https://replicate.delivery/pbxt/GHI124/hvac_bg2.png",
        "https://replicate.delivery/pbxt/GHI125/hvac_bg3.png",
        "https://replicate.delivery/pbxt/GHI126/hvac_bg4.png",
        "https://replicate.delivery/pbxt/GHI127/hvac_bg5.png"
    ],
    "Electrical": [
        "https://replicate.delivery/pbxt/JKL123/electrical_bg1.png",
        "https://replicate.delivery/pbxt/JKL124/electrical_bg2.png",
        "https://replicate.delivery/pbxt/JKL125/electrical_bg3.png",
        "https://replicate.delivery/pbxt/JKL126/electrical_bg4.png",
        "https://replicate.delivery/pbxt/JKL127/electrical_bg5.png"
    ],
    "Landscaping": [
        "https://replicate.delivery/pbxt/MNO123/landscaping_bg1.png",
        "https://replicate.delivery/pbxt/MNO124/landscaping_bg2.png",
        "https://replicate.delivery/pbxt/MNO125/landscaping_bg3.png",
        "https://replicate.delivery/pbxt/MNO126/landscaping_bg4.png",
        "https://replicate.delivery/pbxt/MNO127/landscaping_bg5.png"
    ]
}

def generate_and_cache_backgrounds():
    """ONE-TIME FUNCTION to generate all backgrounds (run locally, then update cache)"""
    business_types = ["Plumbing", "Cleaning", "HVAC", "Electrical", "Landscaping"]
    
    for business_type in business_types:
        st.write(f"🎨 Generating backgrounds for {business_type}...")
        
        backgrounds = []
        for i in range(5):  # Generate 5 backgrounds per business type
            try:
                background = generate_single_background(business_type, i)
                backgrounds.append(background)
                st.write(f"  ✅ Background {i+1} generated")
                time.sleep(2)  # Avoid rate limits
            except Exception as e:
                st.error(f"Failed to generate background {i+1} for {business_type}: {e}")
                # Add fallback background
                backgrounds.append(create_fallback_background(business_type))
        
        BACKGROUND_CACHE[business_type] = backgrounds
    
    st.success("🎉 All backgrounds generated and cached!")

def generate_single_background(business_type, variation):
    """Generate one professional abstract background"""
    
    prompt_variations = {
        "Plumbing": [
            "abstract fluid water flow patterns, blue and silver tones, professional business background, clean modern design, minimalist, corporate marketing graphic, high quality, 4k",
            "modern liquid dynamics abstraction, deep blue tones, professional plumbing background, sleek business design, water theme, minimalist, vector art",
            "contemporary fluid mechanics art, blue and white tones, business marketing background, clean pipes and flow design, abstract, professional",
            "water flow abstraction, aqua blue tones, corporate background, modern plumbing theme, clean lines, business graphic",
            "liquid motion patterns, navy blue and silver, professional service background, abstract water design, marketing material"
        ],
        "Cleaning": [
            "abstract sparkling clean bubbles and waves, white and light green tones, professional hygiene background, pristine clean design, business marketing, minimalist, 4k",
            "modern cleaning abstraction, fresh green and white tones, professional service background, sparkling clean theme, corporate design, vector art",
            "contemporary purity patterns, mint green tones, business cleaning background, sterile clean design, abstract, professional",
            "bubble and foam abstraction, white and teal tones, corporate background, modern cleaning theme, pristine design, business graphic",
            "sparkling clean patterns, light green and white, professional service background, abstract hygiene design, marketing material"
        ],
        "HVAC": [
            "abstract air flow and temperature patterns, blue and white swirls, professional climate control background, modern corporate design, 4k",
            "modern temperature dynamics, cool blue tones, HVAC business background, air flow theme, minimalist, vector art",
            "contemporary climate control abstraction, blue and gray tones, professional service background, ventilation design, abstract",
            "air flow patterns, sky blue tones, corporate background, modern HVAC theme, clean lines, business graphic",
            "temperature gradient abstraction, blue and silver tones, professional service background, abstract climate design, marketing material"
        ],
        "Electrical": [
            "abstract energy flow and circuit patterns, purple and gold lightning effects, professional electrical background, modern tech design, 4k",
            "modern energy dynamics, purple and yellow tones, electrical business background, power flow theme, minimalist, vector art",
            "contemporary circuit abstraction, violet and gold tones, professional service background, electronic design, abstract",
            "energy flow patterns, deep purple tones, corporate background, modern electrical theme, tech design, business graphic",
            "lightning and power abstraction, purple and amber tones, professional service background, abstract energy design, marketing material"
        ],
        "Landscaping": [
            "abstract organic growth and nature patterns, green and earth tones, professional landscaping background, natural business design, 4k",
            "modern nature dynamics, forest green tones, landscaping business background, growth theme, minimalist, vector art",
            "contemporary garden abstraction, green and brown tones, professional service background, organic design, abstract",
            "growth patterns, earthy green tones, corporate background, modern landscaping theme, natural design, business graphic",
            "organic shapes abstraction, green and terracotta tones, professional service background, abstract nature design, marketing material"
        ]
    }
    
    prompts = prompt_variations.get(business_type, ["abstract professional business background, modern corporate design, 4k"])
    prompt = prompts[variation % len(prompts)]
    
    try:
        output = replicate_client.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "negative_prompt": "text, words, letters, people, faces, buildings, realistic photos, messy, cluttered, ugly, blurry",
                "width": 1080,
                "height": 1080,
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 25
            }
        )
        
        if output and len(output) > 0:
            image_url = output[0]
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
                
    except Exception as e:
        st.error(f"Background generation failed: {e}")
    
    return create_fallback_background(business_type)

def create_fallback_background(business_type):
    """Create professional CSS-style background as fallback"""
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    color_schemes = {
        "Plumbing": {"primary": (0, 90, 180), "secondary": (30, 130, 230)},
        "Cleaning": {"primary": (30, 110, 40), "secondary": (80, 180, 120)},
        "Landscaping": {"primary": (40, 120, 45), "secondary": (100, 180, 105)},
        "HVAC": {"primary": (180, 30, 30), "secondary": (220, 70, 70)},
        "Electrical": {"primary": (110, 25, 140), "secondary": (160, 90, 180)}
    }
    
    colors = color_schemes.get(business_type, color_schemes["Plumbing"])
    
    # Create modern gradient background
    for i in range(height):
        r = int(colors["primary"][0] * (1 - i/height) + colors["secondary"][0] * (i/height))
        g = int(colors["primary"][1] * (1 - i/height) + colors["secondary"][1] * (i/height))
        b = int(colors["primary"][2] * (1 - i/height) + colors["secondary"][2] * (i/height))
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    return image

def load_background_image(business_type):
    """Load random background from cache (NO API COSTS!)"""
    backgrounds = BACKGROUND_CACHE.get(business_type, BACKGROUND_CACHE["Plumbing"])
    background_url = random.choice(backgrounds)
    
    try:
        response = requests.get(background_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content)).resize((1080, 1080))
    except:
        pass
    
    # Fallback to generated background if cache fails
    return create_fallback_background(business_type)
    
def load_font(font_name, size):
    """Improved font loading with fallbacks"""
    system_fonts = {
        "Montserrat-Bold.ttf": "arialbd.ttf",
        "Montserrat-Medium.ttf": "arial.ttf", 
        "Montserrat-Regular.ttf": "arial.ttf",
        "Montserrat-SemiBold.ttf": "arialbd.ttf",
        "Montserrat-Light.ttf": "arial.ttf",
        "Montserrat-ExtraBold.ttf": "arialbd.ttf"
    }
    
    system_font = system_fonts.get(font_name, "arial.ttf")
    
    try:
        return ImageFont.truetype(system_font, size)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

# Enhanced Template Functions with AI backgrounds
def create_template_modern(business_type, headline, description, phone_number, colors):
    """Modern Professional Template with AI background"""
    try:
        # Load background image
        background = load_background_image(business_type)
        draw = ImageDraw.Draw(background)
        
        # Add semi-transparent overlay for readability
        overlay = Image.new('RGBA', background.size, (255, 255, 255, 180))
        background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(background)
        
        # Headline with modern styling
        headline_font = load_font("Montserrat-Bold.ttf", 72)
        wrapped_headline = textwrap.fill(headline, width=15)
        draw.text((540, 200), wrapped_headline, fill=colors["primary"], 
                  font=headline_font, anchor="mm", align="center")
        
        # Business badge
        badge_font = load_font("Montserrat-Medium.ttf", 36)
        badge_text = f"{business_type.upper()} SERVICES"
        draw.text((540, 320), badge_text, fill=colors["accent"], font=badge_font, anchor="mm")
        
        # Description with background
        desc_font = load_font("Montserrat-Regular.ttf", 32)
        wrapped_desc = textwrap.fill(description, width=30)
        
        # Add semi-transparent background for description
        desc_bbox = draw.multiline_textbbox((540, 540), wrapped_desc, font=desc_font, anchor="mm")
        padding = 20
        draw.rectangle([desc_bbox[0]-padding, desc_bbox[1]-padding, desc_bbox[2]+padding, desc_bbox[3]+padding], 
                       fill=(255, 255, 255, 200), outline=colors["primary"], width=2)
        
        draw.multiline_text((540, 540), wrapped_desc, fill=(50, 50, 50), 
                           font=desc_font, anchor="mm", align="center")
        
        # Contact section
        contact_font = load_font("Montserrat-SemiBold.ttf", 36)
        draw.text((540, 850), f"📞 {phone_number}", fill=colors["primary"], 
                  font=contact_font, anchor="mm")
        
        return background
        
    except Exception as e:
        st.error(f"Error in modern template: {e}")
        return None

def create_template_minimal(business_type, headline, description, phone_number, colors):
    """Clean & Minimal Template with AI background"""
    try:
        background = load_background_image(business_type)
        draw = ImageDraw.Draw(background)
        
        # Add dark overlay for text readability
        overlay = Image.new('RGBA', background.size, (0, 0, 0, 120))
        background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(background)
        
        # Headline
        headline_font = load_font("Montserrat-Bold.ttf", 64)
        wrapped_headline = textwrap.fill(headline, width=16)
        draw.text((540, 300), wrapped_headline, fill=(255, 255, 255), 
                  font=headline_font, anchor="mm", align="center")
        
        # Separator
        draw.line([(390, 400), (690, 400)], fill=colors["accent"], width=4)
        
        # Description
        desc_font = load_font("Montserrat-Light.ttf", 28)
        wrapped_desc = textwrap.fill(description, width=35)
        draw.multiline_text((540, 550), wrapped_desc, fill=(255, 255, 255), 
                           font=desc_font, anchor="mm", align="center", spacing=10)
        
        # Phone in circle
        phone_font = load_font("Montserrat-SemiBold.ttf", 32)
        circle_center = (540, 800)
        circle_radius = 60
        draw.ellipse([circle_center[0]-circle_radius, circle_center[1]-circle_radius,
                      circle_center[0]+circle_radius, circle_center[1]+circle_radius], 
                     fill=colors["accent"])
        draw.text(circle_center, "📞", fill=(255, 255, 255), font=phone_font, anchor="mm")
        draw.text((540, 880), phone_number, fill=(255, 255, 255), font=phone_font, anchor="mm")
        
        return background
        
    except Exception as e:
        st.error(f"Error in minimal template: {e}")
        return None

def create_template_bold(business_type, headline, description, phone_number, colors):
    """Bold & Energetic Template with AI background"""
    try:
        background = load_background_image(business_type)
        draw = ImageDraw.Draw(background)
        
        # Central content card with shadow effect
        card_width, card_height = 800, 500
        card_x, card_y = 140, 290
        
        # Shadow
        draw.rectangle([card_x+10, card_y+10, card_x+card_width+10, card_y+card_height+10], 
                       fill=(50, 50, 50, 180))
        
        # Main card
        draw.rectangle([card_x, card_y, card_x+card_width, card_y+card_height], 
                       fill=(255, 255, 255), outline=colors["accent"], width=6)
        
        # Headline
        headline_font = load_font("Montserrat-ExtraBold.ttf", 56)
        wrapped_headline = textwrap.fill(headline, width=18)
        draw.multiline_text((540, card_y + 100), wrapped_headline, fill=colors["primary"], 
                           font=headline_font, anchor="mm", align="center")
        
        # Description
        desc_font = load_font("Montserrat-SemiBold.ttf", 28)
        wrapped_desc = textwrap.fill(description, width=32)
        draw.multiline_text((540, card_y + 280), wrapped_desc, fill=(70, 70, 70), 
                           font=desc_font, anchor="mm", align="center", spacing=8)
        
        # Urgent action bar
        action_font = load_font("Montserrat-Black.ttf", 34)
        draw.rectangle([card_x, card_y + card_height - 80, card_x+card_width, card_y+card_height], 
                       fill=colors["accent"])
        draw.text((540, card_y + card_height - 40), f"CALL NOW: {phone_number}", 
                  fill=(255, 255, 255), font=action_font, anchor="mm")
        
        return background
        
    except Exception as e:
        st.error(f"Error in bold template: {e}")
        return None

def create_social_media_graphic(template_type, business_type, headline, description, phone_number):
    """Main function to create social media graphics"""
    color_schemes = {
        "Plumbing": {"primary": (0, 90, 180), "secondary": (30, 130, 230), "accent": (255, 140, 0)},
        "Cleaning": {"primary": (30, 110, 40), "secondary": (80, 180, 120), "accent": (255, 193, 7)},
        "Landscaping": {"primary": (40, 120, 45), "secondary": (100, 180, 105), "accent": (255, 167, 38)},
        "HVAC": {"primary": (180, 30, 30), "secondary": (220, 70, 70), "accent": (66, 133, 244)},
        "Electrical": {"primary": (110, 25, 140), "secondary": (160, 90, 180), "accent": (255, 214, 0)}
    }
    
    colors = color_schemes.get(business_type, color_schemes["Plumbing"])
    
    if template_type == "Modern Professional":
        return create_template_modern(business_type, headline, description, phone_number, colors)
    elif template_type == "Clean & Minimal":
        return create_template_minimal(business_type, headline, description, phone_number, colors)
    elif template_type == "Bold & Energetic":
        return create_template_bold(business_type, headline, description, phone_number, colors)
    else:
        return create_template_modern(business_type, headline, description, phone_number, colors)

# HERO SECTION
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🚀 Create Social Media Graphics That Get Customers</h1>
    <h3 style="font-size: 1.5rem; margin-bottom: 2rem;">Used by 250+ Local Service Businesses</h3>
    <p style="font-size: 1.2rem;">Stop wasting time on design. Generate professional posts in 60 seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric("Graphics Created", "1,234+")
with metric_col2:
    st.metric("Businesses Helped", "250+")
with metric_col3:
    st.metric("Time Saved", "2,100+ hours")

# EXAMPLE GALLERY
st.subheader("🎨 See What You'll Create")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=400", caption="Professional Plumbing Post")
with col2:
    st.image("https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400", caption="Cleaning Service Post") 
with col3:
    st.image("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400", caption="HVAC Service Post")

st.markdown("---")
st.subheader("🚀 How It Works - 3 Simple Steps")
steps_col1, steps_col2, steps_col3 = st.columns(3)
with steps_col1:
    st.markdown("### 1. 📝 Enter Your Details")
    st.write("Business type, phone, custom text")
with steps_col2:
    st.markdown("### 2. 🎨 Choose Template")  
    st.write("Pick from professional designs")
with steps_col3:
    st.markdown("### 3. 📥 Download & Post")
    st.write("Ready-to-use social media graphic")

# TESTIMONIALS
st.subheader("💬 What Business Owners Say")
testimonial_col1, testimonial_col2 = st.columns(2)
with testimonial_col1:
    st.info("""
    **"This tool saved me 5 hours per week! My social media engagement doubled in 30 days."**
    - Mike R., Plumbing Business Owner
    """)
with testimonial_col2:
    st.success("""
    **"Finally, professional graphics without hiring a designer. Worth every penny!"**
    - Sarah L., Cleaning Service
    """)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("💰 Pricing")
    st.write("**Free:** 10 graphics/month")
    st.write("**Pro ($29/month):** Unlimited + AI Content")
    st.write("**Business ($49/month):** White labeling")
    
    st.header("💳 Upgrade Now")
    if st.button("Start $29/month Pro Plan", key="pro_upgrade"):
        st.success("Pro plan selected!")
        st.info("Contact: hello.contentos@gmail.com")
    
    st.header("💡 Need Help?")
    st.write("Email: hello.contentos@gmail.com")
    st.write("24-48 hour response time")

# Main content
tab1, tab2 = st.tabs(["🎨 Create Graphics", "📅 Content Ideas"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        business_type = st.selectbox(
            "Business Type:",
            ["Plumbing", "Cleaning", "Landscaping", "HVAC", "Electrical"],
            key="business_type_main"
        )
        
        template_type = st.selectbox(
            "Design Template:",
            ["Modern Professional", "Clean & Minimal", "Bold & Energetic"],
            key="template_type_main"
        )
        
        # AI Content Generation Buttons
        # Manual Text Input (Clean & Simple)
        phone_number = st.text_input("Phone Number", value="(555) 123-4567", key="phone_main")
        headline = st.text_input("Headline", value=f"Professional {business_type} Services", key="headline_main")
        description = st.text_area("Description", value=f"Expert {business_type} solutions for your home or business. Quality work guaranteed!", key="desc_main")
        
        if st.button("Generate Graphic", type="primary", key="generate_btn"):
            if headline and description and phone_number:
                with st.spinner("Creating your professional graphic..."):
                    try:
                        image = create_social_media_graphic(
                            template_type,
                            business_type, 
                            headline, 
                            description, 
                            phone_number
                        )
                        
                        if image is not None:
                            st.success("✅ Professional graphic created successfully!")
                            
                            # Save and display
                            image_path = f"graphic_{datetime.now().strftime('%H%M%S')}.png"
                            image.save(image_path)
                            
                            st.image(image_path, use_column_width=True, caption="Your Professional Social Media Graphic")
                            
                            # Download button
                            with open(image_path, "rb") as file:
                                st.download_button(
                                    label="📥 Download Graphic",
                                    data=file,
                                    file_name=f"{business_type}_social_media_post.png",
                                    mime="image/png",
                                    key="download_btn"
                                )
                            
                            # Clean up
                            if os.path.exists(image_path):
                                os.remove(image_path)
                        else:
                            st.error("❌ Failed to create graphic. Please try again.")
                        
                    except Exception as e:
                        st.error(f"❌ Error creating graphic: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all fields before generating.")

    with col2:
        st.header("💡 Smart Tips")
        tips = {
            "Plumbing": "• Show before/after photos\n• Highlight emergency services\n• Share water-saving tips\n• Display licensed certifications",
            "Cleaning": "• Post sparkling results\n• Eco-friendly products\n• Seasonal specials\n• Commercial vs residential",
            "Landscaping": "• Garden transformations\n• Lawn care tips\n• Seasonal planting\n• Hardscape features",
            "HVAC": "• Maintenance tips\n• Energy efficiency\n• Emergency repairs\n• System upgrades", 
            "Electrical": "• Safety tips\n• Smart home installs\n• Code compliance\n• Panel upgrades"
        }
        st.write(tips[business_type])
        
        st.header("🎨 Color Scheme")
        color_info = {
            "Plumbing": "Blues & Orange - Trust & urgency",
            "Cleaning": "Greens & Gold - Fresh & premium",
            "Landscaping": "Greens & Earth tones - Natural growth",
            "HVAC": "Reds & Blues - Hot & cold services", 
            "Electrical": "Purple & Gold - Energy & quality"
        }
        st.info(color_info[business_type])

with tab2:
    st.header("30-Day Content Ideas")
    
    # Default content ideas (no AI)
    default_ideas = [
        "Monday: Service highlight of the week",
        "Tuesday: Customer testimonial showcase", 
        "Wednesday: Educational tip or DIY warning",
        "Thursday: Before/after transformation",
        "Friday: Weekend special offer",
        "Saturday: Team spotlight or hiring",
        "Sunday: Industry news or maintenance tip"
    ]
    
    for idea in default_ideas:
        st.write(f"✅ {idea}")
    
    st.download_button(
        label="📥 Download Content Calendar",
        data=json.dumps(default_ideas, indent=2),
        file_name=f"{business_type}_content_calendar.json",
        mime="application/json"
    )

st.success("✨ Ready to generate professional social media graphics!")