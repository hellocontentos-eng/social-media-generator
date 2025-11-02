import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import json
from datetime import datetime, timedelta
import google.generativeai as genai
import requests
from io import BytesIO

# Configure Gemini AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# App configuration
st.set_page_config(
    page_title="Social Media Generator Pro",
    page_icon="🎯",
    layout="wide"
)

# Pre-made background image URLs (using free stock photos)
BACKGROUND_LIBRARY = {
    "Plumbing": [
        "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=800",  # Plumber working
        "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?w=800",  # Plumbing tools
        "https://images.unsplash.com/photo-1581093458791-8a6a5d583c53?w=800",  # Pipe repair
    ],
    "Cleaning": [
        "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800",  # Clean kitchen
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",  # Sparkling bathroom
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800",  # Cleaning supplies
    ],
    "HVAC": [
        "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800",  # AC unit
        "https://images.unsplash.com/photo-1611605698335-8b1569810432?w=800",  # HVAC technician
        "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800",  # Heating system
    ],
    "Electrical": [
        "https://images.unsplash.com/photo-1621905251189-08d45c3c4fdb?w=800",  # Electrician working
        "https://images.unsplash.com/photo-1581093458791-8a6a5d583c53?w=800",  # Electrical panel
        "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800",  # Wiring
    ],
    "Landscaping": [
        "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800",  # Beautiful garden
        "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800",  # Landscaper working
        "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=800",  # Lawn care
    ]
}

def generate_ai_content(business_type, content_type="headline"):
    """Smart AI content generation that finds a working model"""
    
    content_prompts = {
        "headline": f"Create a compelling headline for a {business_type} business social media post. Return only headline.",
        "description": f"Write a short description for a {business_type} company social media post. Return only description.",
    }
    
    try:
        # Get ALL available text generation models
        available_models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
        
        st.write(f"🔍 Found {len(available_models)} text models")
        
        # Try each available model until one works
        for model_name in available_models:
            try:
                st.write(f"🎯 Testing: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(content_prompts[content_type])
                result = response.text.strip().strip('"')
                st.success(f"✅ Working model found: {model_name}")
                return result
            except Exception as e:
                continue  # Try next model
        
        # No models worked
        st.error("❌ No Gemini models worked")
        return get_fallback_content(business_type, content_type)
        
    except Exception as e:
        st.error(f"❌ Model discovery failed: {e}")
        return get_fallback_content(business_type, content_type)

def get_fallback_content(business_type, content_type):
    """Enhanced fallback content for when AI fails"""
    fallback_content = {
        "Plumbing": {
            "headline": "🚰 Emergency Plumbing Services - 24/7 Available",
            "description": "Fast, reliable plumbing solutions! Licensed & insured professionals with upfront pricing."
        },
        "Cleaning": {
            "headline": "✨ Sparkling Clean Results Guaranteed",
            "description": "Professional cleaning services for homes & offices. Eco-friendly products & satisfaction guaranteed!"
        },
        "HVAC": {
            "headline": "❄️ HVAC Services & System Maintenance",
            "description": "Stay comfortable year-round with expert heating & cooling services. Emergency repairs available!"
        },
        "Electrical": {
            "headline": "⚡ Licensed Electrical Services & Repairs", 
            "description": "Safe, reliable electrical solutions for homes and businesses. Code-compliant & insured!"
        },
        "Landscaping": {
            "headline": "🌿 Beautiful Landscaping & Lawn Care",
            "description": "Transform your outdoor space with professional landscaping services. Free consultations available!"
        }
    }
    return fallback_content.get(business_type, {
        "headline": f"Professional {business_type} Services",
        "description": f"Expert {business_type} solutions with quality guaranteed!"
    })[content_type]

def load_background_image(business_type):
    """Load a random background image for the business type"""
    try:
        image_urls = BACKGROUND_LIBRARY.get(business_type, BACKGROUND_LIBRARY["Plumbing"])
        image_url = random.choice(image_urls)
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        return image.resize((1080, 1080))  # Standard social media size
    except:
        # Fallback solid color background
        return Image.new('RGB', (1080, 1080), color=(230, 240, 255))

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
                # AI Content Generation Buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎯 AI Generate Headline", key="ai_headline"):
                st.write("🔍 DEBUG: AI Headline button clicked!")
                with st.spinner("Generating smart headline..."):
                    try:
                        ai_headline = generate_ai_content(business_type, "headline")
                        st.write(f"🔍 DEBUG: AI returned headline: '{ai_headline}'")
                        st.session_state.headline = ai_headline
                        st.write(f"🔍 DEBUG: Session state set to: '{st.session_state.headline}'")
                    except Exception as e:
                        st.error(f"❌ AI Headline Error: {e}")
                        
        with col_b:
            if st.button("📝 AI Generate Description", key="ai_desc"):
                st.write("🔍 DEBUG: AI Description button clicked!")
                with st.spinner("Generating compelling description..."):
                    try:
                        ai_description = generate_ai_content(business_type, "description")
                        st.write(f"🔍 DEBUG: AI returned description: '{ai_description}'")
                        st.session_state.description = ai_description
                        st.write(f"🔍 DEBUG: Session state set to: '{st.session_state.description}'")
                    except Exception as e:
                        st.error(f"❌ AI Description Error: {e}")

        # Debug session state
        st.write("🔍 DEBUG: Current session state:")
        st.write(f"Headline in session: '{st.session_state.get('headline', 'NOT SET')}'")
        st.write(f"Description in session: '{st.session_state.get('description', 'NOT SET')}'")

        phone_number = st.text_input("Phone Number", value="(555) 123-4567", key="phone_main")
        headline = st.text_input("Headline", 
                                value=st.session_state.get('headline', f"Professional {business_type} Services"), 
                                key="headline_main")
        description = st.text_area("Description", 
                                  value=st.session_state.get('description', f"Expert {business_type} solutions for your home or business. Quality work guaranteed!"), 
                                  key="desc_main")
        
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
    
    if st.button("Generate AI Content Calendar", key="ai_calendar"):
        with st.spinner("Creating smart content calendar..."):
            content_ideas = []
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            for day in days:
                idea_prompt = f"Create a social media post idea for a {business_type} business for {day}. Make it engaging and specific to this business type."
                try:
                    ai_idea = generate_ai_content(business_type, "headline")  # Reusing for ideas
                    content_ideas.append(f"{day}: {ai_idea}")
                except:
                    content_ideas.append(f"{day}: Service highlight and special offer")
            
            for idea in content_ideas:
                st.write(f"✅ {idea}")
            
            st.download_button(
                label="📥 Download Content Calendar",
                data=json.dumps(content_ideas, indent=2),
                file_name=f"{business_type}_content_calendar.json",
                mime="application/json"
            )
    else:
        # Default content ideas
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

st.success("✨ Ready to generate professional social media graphics with AI-powered content!")

# Initialize session state
if 'headline' not in st.session_state:
    st.session_state.headline = ""
if 'description' not in st.session_state:
    st.session_state.description = ""