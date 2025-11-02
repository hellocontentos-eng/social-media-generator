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

# ========== ADD GENERATOR FORM RIGHT HERE ==========
st.header("🎨 Create Your First Graphic Now!")

tab1, tab2 = st.tabs(["🎨 Create Graphics", "📅 Content Ideas"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        business_type = st.selectbox(
            "Business Type:",
            ["Plumbing", "Cleaning", "Landscaping", "HVAC", "Electrical"]
        )
        
        # ... REST OF YOUR EXISTING GENERATOR CODE ...
        # Copy all your current form code here

# EXAMPLE GALLERY - Add before the form
# Replace the broken image URLs with these working ones:
st.subheader("🎨 See What You'll Create")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=300", caption="Professional Plumbing Post")
with col2:
    st.image("https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=300", caption="Cleaning Service Post")
with col3:
    st.image("https://images.unsplash.com/photo-1581993192008-63fd1ea7de1a?w=300", caption="HVAC Service Post")
    

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

# Template 1: Modern Professional
def create_template_modern(business_type, headline, description, phone_number, colors):
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Modern gradient background
    for i in range(height):
        r = int(colors["primary"][0] * (1 - i/height) + 255 * (i/height))
        g = int(colors["primary"][1] * (1 - i/height) + 255 * (i/height))
        b = int(colors["primary"][2] * (1 - i/height) + 255 * (i/height))
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Headline with shadow effect
    headline_font = load_font("Montserrat-Bold.ttf", 68)
    wrapped_headline = textwrap.fill(headline, width=18)
    draw.text((width//2, 100), wrapped_headline, fill=(255, 255, 255), 
              font=headline_font, anchor="mm")
    
    # Description box
    desc_font = load_font("Montserrat-Regular.ttf", 32)
    wrapped_desc = textwrap.fill(description, width=35)
    draw.multiline_text((width//2, height//2), wrapped_desc, fill=(50, 50, 50), 
                       font=desc_font, anchor="mm", align="center")
    
    # Contact section
    contact_font = load_font("Montserrat-SemiBold.ttf", 36)
    draw.rectangle([0, height-120, width, height], fill=colors["secondary"])
    draw.text((width//2, height-60), f"Call Today: {phone_number}", fill=(255, 255, 255), 
              font=contact_font, anchor="mm")
    
    return image

# Template 2: Clean & Minimal
def create_template_minimal(business_type, headline, description, phone_number, colors):
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color=(250, 250, 250))
    draw = ImageDraw.Draw(image)
    
    # Top accent bar
    draw.rectangle([0, 0, width, 80], fill=colors["primary"])
    
    # Business type badge
    badge_font = load_font("Montserrat-Medium.ttf", 28)
    badge_text = f"{business_type.upper()} SERVICES"
    draw.text((width//2, 40), badge_text, fill=(255, 255, 255), font=badge_font, anchor="mm")
    
    # Headline
    headline_font = load_font("Montserrat-Bold.ttf", 64)
    wrapped_headline = textwrap.fill(headline, width=20)
    draw.text((width//2, 300), wrapped_headline, fill=colors["primary"], 
              font=headline_font, anchor="mm", align="center")
    
    # Description
    desc_font = load_font("Montserrat-Light.ttf", 30)
    wrapped_desc = textwrap.fill(description, width=40)
    draw.multiline_text((width//2, 550), wrapped_desc, fill=(80, 80, 80), 
                       font=desc_font, anchor="mm", align="center")
    
    # Phone number
    phone_font = load_font("Montserrat-SemiBold.ttf", 32)
    draw.text((width//2, height-70), phone_number, fill=colors["primary"], 
              font=phone_font, anchor="mm")
    
    return image

# Template 3: Bold & Energetic
def create_template_bold(business_type, headline, description, phone_number, colors):
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), color=colors["primary"])
    draw = ImageDraw.Draw(image)
    
    # Central white card
    card_width, card_height = 900, 700
    card_x, card_y = (width - card_width) // 2, (height - card_height) // 2
    draw.rectangle([card_x, card_y, card_x+card_width, card_y+card_height], 
                   fill=(255, 255, 255))
    
    # Headline
    headline_font = load_font("Montserrat-Bold.ttf", 60)
    wrapped_headline = textwrap.fill(headline, width=18)
    draw.multiline_text((width//2, card_y + 150), wrapped_headline, fill=colors["primary"], 
                       font=headline_font, anchor="mm", align="center")
    
    # Description
    desc_font = load_font("Montserrat-Regular.ttf", 28)
    wrapped_desc = textwrap.fill(description, width=35)
    draw.multiline_text((width//2, card_y + 350), wrapped_desc, fill=(70, 70, 70), 
                       font=desc_font, anchor="mm", align="center")
    
    # Urgent action section
    action_font = load_font("Montserrat-Bold.ttf", 36)
    draw.rectangle([card_x, card_y + card_height - 80, card_x+card_width, card_y+card_height], 
                   fill=colors["accent"])
    draw.text((width//2, card_y + card_height - 40), f"CALL NOW: {phone_number}", 
              fill=(255, 255, 255), font=action_font, anchor="mm")
    
    return image

def create_social_media_graphic(template_type, business_type, headline, description, phone_number):
    color_schemes = {
        "Plumbing": {"primary": (0, 100, 200), "secondary": (0, 150, 255), "accent": (255, 100, 0)},
        "Cleaning": {"primary": (0, 150, 100), "secondary": (100, 200, 150), "accent": (255, 200, 0)},
        "Landscaping": {"primary": (0, 120, 0), "secondary": (100, 200, 100), "accent": (200, 150, 0)},
        "HVAC": {"primary": (200, 0, 0), "secondary": (255, 100, 100), "accent": (0, 100, 200)},
        "Electrical": {"primary": (150, 0, 200), "secondary": (200, 100, 255), "accent": (255, 200, 0)}
    }
    
    colors = color_schemes.get(business_type, color_schemes["Plumbing"])
    
    templates = {
        "Modern Professional": create_template_modern,
        "Clean & Minimal": create_template_minimal,
        "Bold & Energetic": create_template_bold
    }
    
    return templates[template_type](business_type, headline, description, phone_number, colors)

# Main app
st.title("🚀 Social Media Generator Pro")
st.subheader("Create professional posts for local service businesses")

# Sidebar
with st.sidebar:
    st.header("💰 Pricing")
    st.write("**Free:** 10 graphics/month")
    st.write("**Pro ($29/month):** Unlimited + AI Content")
    st.write("**Business ($49/month):** White labeling")
    
    # ADD THIS PAYMENT SECTION:
    st.header("💳 Upgrade to Pro")
    if st.button("Start $29/month Pro Plan"):
        st.success("Redirecting to secure checkout...")
        st.info("Payment processing coming soon! For now, contact us at hello.contentos@gmail.com")
    
    # Your existing sidebar content continues below...
    st.header("📝 Customize Your Post")
    business_type = st.selectbox(
        "Business Type:",
        ["Plumbing", "Cleaning", "Landscaping", "HVAC", "Electrical"]
    )
    # ... rest of your existing sidebar code

# Main content
tab1, tab2 = st.tabs(["🎨 Create Graphics", "📅 Content Ideas"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        business_type = st.selectbox(
            "Business Type:",
            ["Plumbing", "Cleaning", "Landscaping", "HVAC", "Electrical"]
        )
        
        template_type = st.selectbox(
            "Design Template:",
            ["Modern Professional", "Clean & Minimal", "Bold & Energetic"]
        )
        
        phone_number = st.text_input("Phone Number", value="(555) 123-4567")
        headline = st.text_input("Headline", value=f"Professional {business_type} Services")
        description = st.text_area("Description", value=f"Expert {business_type} solutions for your home or business. Quality work guaranteed! Contact us today.")
        
        if st.button("Generate Graphic", type="primary"):
            with st.spinner("Creating your graphic..."):
                image = create_social_media_graphic(
                    template_type,
                    business_type, 
                    headline, 
                    description, 
                    phone_number
                )
                
                # Save and display
                image_path = f"output/graphic_{datetime.now().strftime('%H%M%S')}.png"
                os.makedirs("output", exist_ok=True)
                image.save(image_path)
                
                st.image(image_path, use_column_width=True)
                
                # Download button
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Graphic",
                        data=file,
                        file_name=f"{business_type}_social_media.png",
                        mime="image/png"
                    )

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