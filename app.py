import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import json
from datetime import datetime, timedelta
import requests
import time
from io import BytesIO
import plotly.graph_objects as go
import plotly.io as pio
import base64

# ========== BACKGROUND SYSTEM ==========
BACKGROUND_CACHE = {
    "Plumbing": ["backgrounds/plumbing_bg1.jpg"],
    "Cleaning": ["backgrounds/cleaning_bg1.jpg"],
    "HVAC": ["backgrounds/hvac_bg1.jpg"],
    "Electrical": ["backgrounds/electrical_bg1.jpg"],
    "Landscaping": ["backgrounds/landscaping_bg1.jpg"]
}

def load_background_image(business_type):
    """Load random background from local files"""
    backgrounds = BACKGROUND_CACHE.get(business_type, BACKGROUND_CACHE["Plumbing"])
    background_path = random.choice(backgrounds)
    
    try:
        image = Image.open(background_path)
        return image.resize((1080, 1080))
    except Exception as e:
        st.error(f"❌ Failed to load {background_path}: {e}")
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
    
    for i in range(height):
        r = int(colors["primary"][0] * (1 - i/height) + colors["secondary"][0] * (i/height))
        g = int(colors["primary"][1] * (1 - i/height) + colors["secondary"][1] * (i/height))
        b = int(colors["primary"][2] * (1 - i/height) + colors["secondary"][2] * (i/height))
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    return image

# ========== PLOTLY TEMPLATE SYSTEM ==========
def create_plotly_template(business_type, headline, description, phone_number, colors):
    """Create professional social media graphic using Plotly"""
    try:
        # Load background image
        background = load_background_image(business_type)
        
        # Convert PIL Image to base64 for Plotly
        buffered = BytesIO()
        background.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        background_url = f"data:image/png;base64,{img_str}"
        
        # Create figure
        fig = go.Figure()
        
        # Add background image
        fig.add_layout_image(
            dict(
                source=background_url,
                xref="paper", yref="paper",
                x=0, y=1, sizex=1, sizey=1,
                sizing="stretch",
                layer="below"
            )
        )
        
        # 1. HEADLINE (Top - Large & Bold)
        fig.add_annotation(
            dict(
                x=0.5, y=0.78,
                xref="paper", yref="paper",
                text=f"<b>{headline}</b>",
                showarrow=False,
                font=dict(
                    size=65,
                    color=f"rgb{colors['primary']}",
                    family="Arial, sans-serif"
                ),
                align="center",
                bordercolor=f"rgb{colors['primary']}",
                borderwidth=2,
                borderpad=10,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )
        
        # 2. BUSINESS TYPE (Below Headline)
        fig.add_annotation(
            dict(
                x=0.5, y=0.63,
                xref="paper", yref="paper",
                text=f"<b>{business_type.upper()} SERVICES</b>",
                showarrow=False,
                font=dict(
                    size=42,
                    color=f"rgb{colors['accent']}",
                    family="Arial, sans-serif"
                ),
                align="center",
                bordercolor=f"rgb{colors['accent']}",
                borderwidth=1,
                borderpad=8,
                bgcolor="rgba(255,255,255,0.9)"
            )
        )
        
        # 3. DESCRIPTION (Middle)
        fig.add_annotation(
            dict(
                x=0.5, y=0.45,
                xref="paper", yref="paper",
                text=f"<i>{description}</i>",
                showarrow=False,
                font=dict(
                    size=38,
                    color="rgb(50,50,50)",
                    family="Arial, sans-serif"
                ),
                align="center",
                bordercolor="rgb(100,100,100)",
                borderwidth=1,
                borderpad=10,
                bgcolor="rgba(255,255,255,0.85)"
            )
        )
        
        # 4. PHONE NUMBER (Bottom)
        fig.add_annotation(
            dict(
                x=0.5, y=0.25,
                xref="paper", yref="paper",
                text=f"<b>📞 Call Now: {phone_number}</b>",
                showarrow=False,
                font=dict(
                    size=44,
                    color=f"rgb{colors['primary']}",
                    family="Arial, sans-serif"
                ),
                align="center",
                bordercolor=f"rgb{colors['primary']}",
                borderwidth=2,
                borderpad=12,
                bgcolor="rgba(255,255,255,0.9)"
            )
        )
        
        # Set layout
        fig.update_layout(
            width=1080,
            height=1080,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1])
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Plotly template error: {e}")
        return None

def fig_to_image(fig):
    """Convert Plotly figure to PIL Image"""
    try:
        # Convert to image bytes
        img_bytes = pio.to_image(fig, format="png", width=1080, height=1080)
        # Convert to PIL Image
        return Image.open(BytesIO(img_bytes))
    except Exception as e:
        st.error(f"Image conversion error: {e}")
        return None
def create_social_media_graphic(template_type, business_type, headline, description, phone_number):
    """Main function to create social media graphics using Plotly"""
    color_schemes = {
        "Plumbing": {"primary": (0, 90, 180), "accent": (255, 140, 0)},
        "Cleaning": {"primary": (30, 110, 40), "accent": (255, 193, 7)},
        "Landscaping": {"primary": (40, 120, 45), "accent": (255, 167, 38)},
        "HVAC": {"primary": (180, 30, 30), "accent": (66, 133, 244)},
        "Electrical": {"primary": (110, 25, 140), "accent": (255, 214, 0)}
    }
    
    colors = color_schemes.get(business_type, color_schemes["Plumbing"])
    
    # Create Plotly template
    fig = create_plotly_template(business_type, headline, description, phone_number, colors)
    
    if fig:
        return fig_to_image(fig)
    return None
    
# App configuration
st.set_page_config(
    page_title="Social Media Generator Pro",
    page_icon="🎯",
    layout="wide"
)

# Plotly Debug Function
def debug_plotly_system():
    st.sidebar.header("🔍 Plotly System Check")
    
    if st.sidebar.button("Test Plotly Template"):
        try:
            test_fig = create_plotly_template(
                "Plumbing",
                "Test Headline",
                "Test description",
                "(555) 123-4567", 
                {"primary": (0, 90, 180), "accent": (255, 140, 0)}
            )
            if test_fig:
                test_img = fig_to_image(test_fig)
                st.sidebar.image(test_img, caption="Plotly Test", use_column_width=True)
                st.sidebar.success("✅ Plotly system works!")
            else:
                st.sidebar.error("❌ Plotly template failed")
        except Exception as e:
            st.sidebar.error(f"❌ Plotly error: {e}")

# Call the debug function
debug_plotly_system()
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
    """Load random background from local files (FREE & RELIABLE)"""
    backgrounds = BACKGROUND_CACHE.get(business_type, BACKGROUND_CACHE["Plumbing"])
    background_path = random.choice(backgrounds)
    
    # DEBUG: Show what path is being used
    try:
        image = Image.open(background_path)
        return image.resize((1080, 1080))
    except Exception as e:
        st.error(f"❌ Failed to load {background_path}: {e}")
        # If local file fails, use fallback background
        return create_fallback_background(business_type)
        

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

try:
    # Create sample graphics using Plotly
    sample1_fig = create_plotly_template(
        "Plumbing",
        "Emergency Plumbing",
        "Fast & reliable service",
        "(555) 123-4567",
        {"primary": (0, 90, 180), "accent": (255, 140, 0)}
    )
    
    sample2_fig = create_plotly_template(
        "Cleaning", 
        "Sparkling Clean",
        "Professional results",
        "(555) 123-4567",
        {"primary": (30, 110, 40), "accent": (255, 193, 7)}
    )
    
    sample3_fig = create_plotly_template(
        "HVAC",
        "Climate Experts", 
        "Comfort you can trust",
        "(555) 123-4567",
        {"primary": (180, 30, 30), "accent": (66, 133, 244)}
    )
    
    # Convert to images for display
    sample1_img = fig_to_image(sample1_fig) if sample1_fig else None
    sample2_img = fig_to_image(sample2_fig) if sample2_fig else None  
    sample3_img = fig_to_image(sample3_fig) if sample3_fig else None
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if sample1_img:
            st.image(sample1_img, caption="Professional Plumbing Post", use_column_width=True)
    with col2:
        if sample2_img:
            st.image(sample2_img, caption="Cleaning Service Post", use_column_width=True)
    with col3:
        if sample3_img:
            st.image(sample3_img, caption="HVAC Service Post", use_column_width=True)
        
except Exception as e:
    st.error(f"Could not create sample graphics: {e}")
    
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