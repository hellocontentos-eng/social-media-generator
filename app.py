import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
from datetime import datetime

# ---------------- App Config ----------------
st.set_page_config(
    page_title="Social Media Generator Pro",
    page_icon="🎯",
    layout="wide"
)

# ---------------- Hero Section ----------------
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🚀 Create Social Media Graphics That Get Customers</h1>
    <h3 style="font-size: 1.5rem; margin-bottom: 2rem;">Used by 250+ Local Service Businesses</h3>
    <p style="font-size: 1.2rem;">Stop wasting time on design. Generate professional posts in 60 seconds.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Metrics ----------------
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Graphics Created", "1,234+", key="metric_graphics")
metric_col2.metric("Businesses Helped", "250+", key="metric_businesses")
metric_col3.metric("Time Saved", "2,100+ hours", key="metric_time_saved")

st.markdown("---")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("💰 Pricing")
    st.write("**Free:** 10 graphics/month", key="sidebar_free_plan")
    st.write("**Pro ($29/month):** Unlimited + AI Content", key="sidebar_pro_plan")
    st.write("**Business ($49/month):** White labeling", key="sidebar_business_plan")
    
    st.header("💳 Upgrade Now")
    if st.button("Start $29/month Pro Plan", key="sidebar_pro_upgrade"):
        st.success("Pro plan selected!")
        st.info("Contact: hello.contentos@gmail.com")
    
    st.header("💡 Need Help?")
    st.write("Email: hello.contentos@gmail.com", key="sidebar_help_email")
    st.write("24-48 hour response time", key="sidebar_help_response")

# ---------------- Helper Functions ----------------
def load_font(font_name, size):
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
        return ImageFont.load_default()

def create_social_media_graphic(template_type, business_type, headline, description, phone_number, hashtags_list=[]):
    width, height = 800, 800
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Background
    draw.rectangle([0,0,width,height], fill=(240,240,240))
    
    # Headline
    draw.text((width//2, 150), headline, fill=(0,0,0), font=load_font("Montserrat-Bold.ttf", 48), anchor="mm")
    
    # Description + hashtags
    full_text = description + ("\n" + " ".join(hashtags_list) if hashtags_list else "")
    draw.multiline_text((width//2, 300), full_text, fill=(50,50,50), font=load_font("Montserrat-Regular.ttf", 28), anchor="mm", align="center")
    
    # Phone
    draw.text((width//2, height-100), f"📞 {phone_number}", fill=(0,0,0), font=load_font("Montserrat-SemiBold.ttf", 32), anchor="mm")
    
    return image

# Dummy AI copy function
def generate_ai_copy(business_type):
    return {
        "headline": f"Top {business_type} Services Near You!",
        "description": f"Get the best {business_type} solutions with guaranteed quality.",
        "hashtags": ["#LocalBusiness", f"#{business_type.replace(' ','')}", "#Professional"]
    }

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["🎨 Create Graphics", "📅 Content Ideas"])

# ---------------- Tab 1 ----------------
with tab1:
    tab1_container = st.container()
    with tab1_container:
        col1, col2 = st.columns([2,1])
        with col1:
            # --- Business & Template Selection ---
            business_type = st.selectbox(
                "Business Type:", 
                ["Plumbing", "Cleaning", "Landscaping", "HVAC", "Electrical"], 
                key="tab1_business_type"
            )
            template_type = st.selectbox(
                "Design Template:", 
                ["Modern Professional", "Clean & Minimal", "Bold & Energetic"], 
                key="tab1_template_type"
            )

            # --- Session-state safe defaults ---
            if "tab1_phone" not in st.session_state:
                st.session_state.tab1_phone = "(555) 123-4567"
            if "tab1_headline" not in st.session_state:
                st.session_state.tab1_headline = f"Professional {business_type} Services"
            if "tab1_description" not in st.session_state:
                st.session_state.tab1_description = f"Expert {business_type} solutions for your home or business. Quality work guaranteed! Contact us today."

            # --- Text Inputs ---
            phone_number = st.text_input("Phone Number", value=st.session_state.tab1_phone, key="tab1_phone_input")
            st.session_state.tab1_phone = phone_number

            headline = st.text_input("Headline", value=st.session_state.tab1_headline, key="tab1_headline_input")
            st.session_state.tab1_headline = headline

            description = st.text_area("Description", value=st.session_state.tab1_description, key="tab1_description_input")
            st.session_state.tab1_description = description

            # --- AI Suggest ---
            if st.button("💡 Suggest AI Text", key="tab1_ai_suggest"):
                ai_result = generate_ai_copy(business_type)
                st.session_state.tab1_headline = ai_result["headline"]
                st.session_state.tab1_description = ai_result["description"] + "\n" + " ".join(ai_result["hashtags"])
                st.success("✅ AI suggestion generated!")
                st.write("**Headline:**", st.session_state.tab1_headline)
                st.write("**Description + Hashtags:**", st.session_state.tab1_description)

            # --- Generate Graphic ---
            if "generate_clicked" not in st.session_state:
                st.session_state.generate_clicked = False

            generate_placeholder = st.empty()
            with generate_placeholder:
                if st.button("Generate Graphic", type="primary", key="tab1_generate_graphic"):
                    st.session_state.generate_clicked = True

        # --- Tips Column ---
        with col2:
            st.header("💡 Tips")
            tips = {
                "Plumbing": "• Show before/after photos\n• Highlight emergency services\n• Share water-saving tips",
                "Cleaning": "• Post sparkling results\n• Eco-friendly products\n• Seasonal specials",
                "Landscaping": "• Garden transformations\n• Lawn care tips\n• Seasonal planting",
                "HVAC": "• Maintenance tips\n• Energy efficiency\n• Emergency repairs",
                "Electrical": "• Safety tips\n• Smart home installs\n• Code compliance"
            }
            st.write(tips[business_type], key="tab1_tips")

    # Generate Graphic if clicked
    if st.session_state.generate_clicked:
        hashtags_list = [tag for tag in st.session_state.tab1_description.split() if tag.startswith("#")]
        image = create_social_media_graphic(template_type, business_type, st.session_state.tab1_headline, st.session_state.tab1_description, st.session_state.tab1_phone, hashtags_list)
        os.makedirs("output", exist_ok=True)
        image_path = f"output/graphic_{datetime.now().strftime('%H%M%S')}.png"
        image.save(image_path)
        st.image(image_path, use_column_width=True, caption="Your Professional Social Media Graphic")
        with open(image_path, "rb") as file:
            st.download_button("📥 Download Graphic", file, file_name=f"{business_type}_social_media_post.png", mime="image/png", key="tab1_download_btn")

# ---------------- Tab 2 ----------------
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
    for idx, idea in enumerate(content_ideas):
        st.write(f"✅ {idea}", key=f"tab2_idea_{idx}")
    st.download_button("📥 Download Content Calendar", data=json.dumps(content_ideas, indent=2), file_name="content_calendar.json", mime="application/json", key="tab2_download_calendar")

st.success("✨ Ready to generate professional social media graphics!")
