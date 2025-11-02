import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import json
from datetime import datetime, timedelta

# App configuration
st.set_page_config(
    page_title="Social Media Generator Pro",
    page_icon="🎯",
    layout="wide"
)

    
# HERO SECTION (your current code)
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🚀 Create Social Media Graphics That Get Customers</h1>
    <h3 style="font-size: 1.5rem; margin-bottom: 2rem;">Used by 250+ Local Service Businesses</h3>
    <p style="font-size: 1.2rem;">Stop wasting time on design. Generate professional posts in 60 seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
# Add below hero section
st.markdown("---")
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric("Graphics Created", "1,234+")
with metric_col2:
    st.metric("Businesses Helped", "250+")
with metric_col3:
    st.metric("Time Saved", "2,100+ hours")

# EXAMPLE GALLERY - Replace with working images
st.subheader("🎨 See What You'll Create")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://picsum.photos/300/300?random=1", caption="Professional Plumbing Post")
with col2:
    st.image("https://picsum.photos/300/300?random=2", caption="Cleaning Service Post") 
with col3:
    st.image("https://picsum.photos/300/300?random=3", caption="HVAC Service Post")

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
st.subheader("💰 Choose Your Plan")

pricing_col1, pricing_col2, pricing_col3 = st.columns(3)

with pricing_col1:
    st.markdown("### 🆓 Starter")
    st.write("**$0/month**")
    st.write("• 10 graphics/month")
    st.write("• Basic templates")
    st.write("• Standard support")
    
with pricing_col2:
    st.markdown("### ⭐ Pro")
    st.write("**$29/month**")
    st.write("• Unlimited graphics")
    st.write("• All templates + AI")
    st.write("• Priority support")
    
with pricing_col3:
    st.markdown("### 🏢 Business")
    st.write("**$49/month**")
    st.write("• White labeling")
    st.write("• Custom templates")
    st.write("• Dedicated support")
    

st.markdown("---")
st.subheader("❓ Frequently Asked Questions")

with st.expander("How many graphics can I create?"):
    st.write("Free plan: 10/month | Pro/Business: Unlimited")
    
with st.expander("What social media platforms are supported?"):
    st.write("All platforms: Instagram, Facebook, LinkedIn, Twitter")
    
with st.expander("Can I use my own branding?"):
    st.write("Yes! Business plan includes custom colors and logos")
    
    
# Load fonts
def load_font(font_name, size):
    font_path = os.path.join("fonts", font_name)
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

# Template 1: Modern Professional (Enhanced)
def create_template_modern(business_type, headline, description, phone_number, colors):
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Modern gradient background
    for i in range(height):
        r = int(colors["primary"][0] * (1 - i/height) + 230 * (i/height))
        g = int(colors["primary"][1] * (1 - i/height) + 230 * (i/height))
        b = int(colors["primary"][2] * (1 - i/height) + 230 * (i/height))
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Decorative elements
    draw.rectangle([0, 0, width, 120], fill=colors["primary"])
    draw.rectangle([0, height-100, width, height], fill=colors["secondary"])
    
    # Headline with better styling
    headline_font = load_font("Montserrat-Bold.ttf", 72)
    wrapped_headline = textwrap.fill(headline, width=15)
    draw.text((width//2, 60), wrapped_headline, fill=(255, 255, 255), 
              font=headline_font, anchor="mm", stroke_width=2, stroke_fill=(100, 100, 100))
    
    # Business badge
    badge_font = load_font("Montserrat-Medium.ttf", 36)
    badge_text = f"{business_type.upper()} SERVICES"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0] + 40
    draw.rectangle([width//2 - badge_width//2, 180, width//2 + badge_width//2, 230], 
                   fill=colors["accent"])
    draw.text((width//2, 205), badge_text, fill=(255, 255, 255), font=badge_font, anchor="mm")
    
    # Description with background
    desc_font = load_font("Montserrat-Regular.ttf", 36)
    wrapped_desc = textwrap.fill(description, width=30)
    
    # Add semi-transparent background for description
    desc_bbox = draw.multiline_textbbox((width//2, height//2), wrapped_desc, font=desc_font, anchor="mm")
    padding = 30
    draw.rectangle([desc_bbox[0]-padding, desc_bbox[1]-padding, desc_bbox[2]+padding, desc_bbox[3]+padding], 
                   fill=(255, 255, 255, 200), outline=colors["primary"], width=3)
    
    draw.multiline_text((width//2, height//2), wrapped_desc, fill=(50, 50, 50), 
                       font=desc_font, anchor="mm", align="center")
    
    # Contact section with icon
    contact_font = load_font("Montserrat-SemiBold.ttf", 40)
    draw.text((width//2, height-50), f"📞 Call Today: {phone_number}", fill=(255, 255, 255), 
              font=contact_font, anchor="mm")
    
    return image

# Template 2: Clean & Minimal (Enhanced)
def create_template_minimal(business_type, headline, description, phone_number, colors):
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color=(248, 248, 248))
    draw = ImageDraw.Draw(image)
    
    # Top accent bar with pattern
    draw.rectangle([0, 0, width, 100], fill=colors["primary"])
    
    # Business type with icon
    badge_font = load_font("Montserrat-Medium.ttf", 32)
    icons = {"Plumbing": "🔧", "Cleaning": "✨", "Landscaping": "🌿", "HVAC": "❄️", "Electrical": "⚡"}
    badge_text = f"{icons.get(business_type, '🏢')} {business_type.upper()} SERVICES"
    draw.text((width//2, 50), badge_text, fill=(255, 255, 255), font=badge_font, anchor="mm")
    
    # Headline with accent color
    headline_font = load_font("Montserrat-Bold.ttf", 68)
    wrapped_headline = textwrap.fill(headline, width=16)
    draw.text((width//2, 280), wrapped_headline, fill=colors["primary"], 
              font=headline_font, anchor="mm", align="center")
    
    # Decorative separator
    draw.line([(width//4, 380), (3*width//4, 380)], fill=colors["accent"], width=4)
    
    # Description in elegant layout
    desc_font = load_font("Montserrat-Light.ttf", 32)
    wrapped_desc = textwrap.fill(description, width=35)
    draw.multiline_text((width//2, 550), wrapped_desc, fill=(80, 80, 80), 
                       font=desc_font, anchor="mm", align="center", spacing=10)
    
    # Contact in circle design
    phone_font = load_font("Montserrat-SemiBold.ttf", 36)
    circle_center = (width//2, height-180)
    circle_radius = 80
    draw.ellipse([circle_center[0]-circle_radius, circle_center[1]-circle_radius,
                  circle_center[0]+circle_radius, circle_center[1]+circle_radius], 
                 fill=colors["accent"], outline=colors["primary"], width=3)
    draw.text(circle_center, "📞", fill=(255, 255, 255), font=phone_font, anchor="mm")
    
    # Phone number below circle
    draw.text((width//2, height-70), phone_number, fill=colors["primary"], 
              font=phone_font, anchor="mm")
    
    return image

# Template 3: Bold & Energetic
# Template 3: Bold & Energetic (Enhanced)
def create_template_bold(business_type, headline, description, phone_number, colors):
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color=colors["primary"])
    draw = ImageDraw.Draw(image)
    
    # Dynamic background pattern
    for i in range(0, width, 60):
        draw.line([(i, 0), (i, height)], fill=colors["secondary"], width=2, joint="curve")
    for i in range(0, height, 60):
        draw.line([(0, i), (width, i)], fill=colors["secondary"], width=2, joint="curve")
    
    # Central white card with shadow effect
    card_width, card_height = 850, 650
    card_x, card_y = (width - card_width) // 2, (height - card_height) // 2
    
    # Shadow effect
    shadow_offset = 15
    draw.rectangle([card_x+shadow_offset, card_y+shadow_offset, 
                    card_x+card_width+shadow_offset, card_y+card_height+shadow_offset], 
                   fill=(50, 50, 50))
    
    # Main card
    draw.rectangle([card_x, card_y, card_x+card_width, card_y+card_height], 
                   fill=(255, 255, 255), outline=colors["accent"], width=8)
    
    # Business icon and title
    icon_font = load_font("Montserrat-Bold.ttf", 48)
    icons = {"Plumbing": "🔧", "Cleaning": "✨", "Landscaping": "🌿", "HVAC": "❄️", "Electrical": "⚡"}
    icon_text = f"{icons.get(business_type, '🏢')} {business_type.upper()}"
    draw.text((width//2, card_y + 80), icon_text, fill=colors["primary"], 
              font=icon_font, anchor="mm")
    
    # Headline with impact
    headline_font = load_font("Montserrat-ExtraBold.ttf", 64)
    wrapped_headline = textwrap.fill(headline, width=16)
    draw.multiline_text((width//2, card_y + 200), wrapped_headline, fill=colors["primary"], 
                       font=headline_font, anchor="mm", align="center", stroke_width=2, stroke_fill=(200, 200, 200))
    
    # Separator line
    draw.line([(card_x + 100, card_y + 280), (card_x + card_width - 100, card_y + 280)], 
              fill=colors["accent"], width=5)
    
    # Description
    desc_font = load_font("Montserrat-SemiBold.ttf", 30)
    wrapped_desc = textwrap.fill(description, width=32)
    draw.multiline_text((width//2, card_y + 380), wrapped_desc, fill=(70, 70, 70), 
                       font=desc_font, anchor="mm", align="center", spacing=12)
    
    # Urgent action section
    action_font = load_font("Montserrat-Black.ttf", 38)
    draw.rectangle([card_x, card_y + card_height - 100, card_x+card_width, card_y+card_height], 
                   fill=colors["accent"])
    
    # Call-to-action text
    draw.text((width//2, card_y + card_height - 60), f"📞 CALL NOW FOR FREE ESTIMATE", 
              fill=(255, 255, 255), font=action_font, anchor="mm")
    
    # Phone number emphasized
    phone_font = load_font("Montserrat-Bold.ttf", 42)
    draw.text((width//2, card_y + card_height - 20), phone_number, 
              fill=(255, 255, 255), font=phone_font, anchor="mm")
    
    return image

def create_social_media_graphic(template_type, business_type, headline, description, phone_number):
    color_schemes = {
        "Plumbing": {"primary": (0, 90, 180), "secondary": (30, 130, 230), "accent": (255, 140, 0)},
        "Cleaning": {"primary": (30, 110, 40), "secondary": (80, 180, 120), "accent": (255, 193, 7)},
        "Landscaping": {"primary": (40, 120, 45), "secondary": (100, 180, 105), "accent": (255, 167, 38)},
        "HVAC": {"primary": (180, 30, 30), "secondary": (220, 70, 70), "accent": (66, 133, 244)},
        "Electrical": {"primary": (110, 25, 140), "secondary": (160, 90, 180), "accent": (255, 214, 0)}
    }
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
            key="business_type_main"  # ← CORRECT KEY
        )
        
        template_type = st.selectbox(
            "Design Template:",
            ["Modern Professional", "Clean & Minimal", "Bold & Energetic"],
            key="template_type_main"
        )
        
        phone_number = st.text_input("Phone Number", value="(555) 123-4567", key="phone_main")
        headline = st.text_input("Headline", value=f"Professional {business_type} Services", key="headline_main")
        description = st.text_area("Description", value=f"Expert {business_type} solutions for your home or business. Quality work guaranteed! Contact us today.", key="desc_main")
        
        if st.button("Generate Graphic", type="primary", key="generate_btn"):
            if headline and description and phone_number:
                with st.spinner("Creating your professional graphic..."):
                    try:
                        # DEBUG: Show what values are being used
                        st.write(f"🔧 Debug: Business={business_type}, Template={template_type}")
                        st.write(f"🔧 Debug: Headline='{headline}'")
                        
                        image = create_social_media_graphic(
                            template_type,
                            business_type, 
                            headline, 
                            description, 
                            phone_number
                        )
                        
                        st.success("✅ Image created successfully!")
                        
                        # Save and display
                        image_path = f"output/graphic_{datetime.now().strftime('%H%M%S')}.png"
                        os.makedirs("output", exist_ok=True)
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
                        
                    except Exception as e:
                        st.error(f"❌ Error creating graphic: {str(e)}")
                        st.info("Please check if all fonts are properly installed.")
            else:
                st.warning("⚠️ Please fill in all fields before generating.")

    with col2:
        st.header("💡 Tips")
        tips = {
            "Plumbing": "• Show before/after photos\n• Highlight emergency services\n• Share water-saving tips",
            "Cleaning": "• Post sparkling results\n• Eco-friendly products\n• Seasonal specials",
            "Landscaping": "• Garden transformations\n• Lawn care tips\n• Seasonal planting",
            "HVAC": "• Maintenance tips\n• Energy efficiency\n• Emergency repairs", 
            "Electrical": "• Safety tips\n• Smart home installs\n• Code compliance"
        }
        st.write(tips[business_type])

with tab2:
    st.header("30-Day Content Ideas")
    
    content_ideas = [
        "Monday: Service highlight of the week",
        "Tuesday: Customer testimonial", 
        "Wednesday: Educational tip",
        "Thursday: Before/after transformation",
        "Friday: Weekend special offer",
        "Saturday: Team spotlight",
        "Sunday: Industry news"
    ]
    
    for idea in content_ideas:
        st.write(f"✅ {idea}")
    
    st.download_button(
        label="📥 Download Content Calendar",
        data=json.dumps(content_ideas, indent=2),
        file_name="content_calendar.json",
        mime="application/json"
    )

st.success("✨ Ready to generate professional social media graphics!")