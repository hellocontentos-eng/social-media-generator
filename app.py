import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import json
from datetime import datetime

# ==== AI Text Integration ====
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_ai_copy(business_type, tone="Professional"):
    prompt = f"""
    You are a social media copywriting expert.
    Write a catchy headline and 2-line post description for a {business_type} business.
    Tone: {tone}.
    Include 3 relevant hashtags.
    Respond ONLY in JSON format:
    {{ "headline": "...", "description": "...", "hashtags": ["#","#","#"] }}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        st.error(f"AI text generation failed: {e}")
        return {"headline": "", "description": "", "hashtags": []}


# ==== Streamlit Config ====
st.set_page_config(
    page_title="Social Media Generator Pro",
    page_icon="🎯",
    layout="wide"
)

# Hero section
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🚀 Create Social Media Graphics That Get Customers</h1>
    <h3 style="font-size: 1.5rem; margin-bottom: 2rem;">Used by 250+ Local Service Businesses</h3>
    <p style="font-size: 1.2rem;">Stop wasting time on design. Generate professional posts in 60 seconds.</p>
</div>
""", unsafe_allow_html=True)

# Metrics
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Graphics Created", "1,234+", key="metric_graphics")
metric_col2.metric("Businesses Helped", "250+", key="metric_businesses")
metric_col3.metric("Time Saved", "2,100+ hours", key="metric_time_saved")

# ==== Example Gallery ====
st.subheader("🎨 See What You'll Create")
col1, col2, col3 = st.columns(3)
with col1: st.image("https://picsum.photos/300/300?random=1", caption="Professional Plumbing Post")
with col2: st.image("https://picsum.photos/300/300?random=2", caption="Cleaning Service Post")
with col3: st.image("https://picsum.photos/300/300?random=3", caption="HVAC Service Post")

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

# ==== Testimonials ====
st.subheader("💬 What Business Owners Say")
testimonial_col1, testimonial_col2 = st.columns(2)
with testimonial_col1:
    st.info("**\"This tool saved me 5 hours per week! My social media engagement doubled in 30 days.\"** - Mike R., Plumbing Business Owner")
with testimonial_col2:
    st.success("**\"Finally, professional graphics without hiring a designer. Worth every penny!\"** - Sarah L., Cleaning Service")

st.markdown("---")

# ==== Pricing ====
st.subheader("💰 Choose Your Plan")
pricing_col1, pricing_col2, pricing_col3 = st.columns(3)
with pricing_col1:
    st.markdown("### 🆓 Starter\n**$0/month**\n• 10 graphics/month\n• Basic templates\n• Standard support")
with pricing_col2:
    st.markdown("### ⭐ Pro\n**$29/month**\n• Unlimited graphics\n• All templates + AI\n• Priority support")
with pricing_col3:
    st.markdown("### 🏢 Business\n**$49/month**\n• White labeling\n• Custom templates\n• Dedicated support")

st.markdown("---")

# ==== FAQs ====
st.subheader("❓ Frequently Asked Questions")
with st.expander("How many graphics can I create?"):
    st.write("Free plan: 10/month | Pro/Business: Unlimited")
with st.expander("What social media platforms are supported?"):
    st.write("All platforms: Instagram, Facebook, LinkedIn, Twitter")
with st.expander("Can I use my own branding?"):
    st.write("Yes! Business plan includes custom colors and logos")

# ==== Font Loader & Template Functions ====
def load_font(font_name, size):
    try:
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

# Simple Modern Template Example
def create_template_modern(business_type, headline, description, phone_number, colors, hashtags=None):
    """Modern Professional Template with optional hashtags"""
    try:
        width, height = 800, 800
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Simple gradient background
        for i in range(height):
            r = int(colors["primary"][0] * (1 - i/height) + 230 * (i/height))
            g = int(colors["primary"][1] * (1 - i/height) + 230 * (i/height))
            b = int(colors["primary"][2] * (1 - i/height) + 230 * (i/height))
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        # Fonts
        headline_font = load_font("Montserrat-Bold.ttf", 48)
        desc_font = load_font("Montserrat-Regular.ttf", 28)
        phone_font = load_font("Montserrat-SemiBold.ttf", 32)
        hashtags_font = load_font("Montserrat-Medium.ttf", 24)

        # Headline
        draw.multiline_text((width//2, 100), textwrap.fill(headline, width=20),
                            fill=(0,0,0), font=headline_font, anchor="mm", align="center")
        
        # Description
        draw.multiline_text((width//2, 350), textwrap.fill(description, width=35),
                            fill=(50,50,50), font=desc_font, anchor="mm", align="center")
        
        # Phone
        draw.text((width//2, height-120), f"📞 {phone_number}",
                  fill=colors["accent"], font=phone_font, anchor="mm")
        
        # Optional Hashtags
        if hashtags:
            hashtags_text = " ".join(hashtags)
            draw.text((width//2, height-60), hashtags_text,
                      fill=(80, 80, 80), font=hashtags_font, anchor="mm")
        
        return image
    
    except Exception as e:
        st.error(f"Error in modern template: {e}")
        return None


def create_social_media_graphic(template_type, business_type, headline, description, phone_number, hashtags=None):
    colors = {"primary": (0, 90, 180), "accent": (255, 140, 0)}
    
    if template_type == "Modern Professional":
        return create_template_modern(business_type, headline, description, phone_number, colors, hashtags)
    # Add your other templates (Minimal, Bold) here if you want hashtags too
    else:
        return create_template_modern(business_type, headline, description, phone_number, colors, hashtags)


# ==== Sidebar ====
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


# ==== Main Content Tabs ====
tab1, tab2 = st.tabs(["🎨 Create Graphics", "📅 Content Ideas"])

with tab1:
    col1, col2 = st.columns([2, 1])

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

        # --- Initialize session state safely ---
        if "tab1_phone" not in st.session_state:
            st.session_state.tab1_phone = "(555) 123-4567"
        if "tab1_headline" not in st.session_state:
            st.session_state.tab1_headline = f"Professional {business_type} Services"
        if "tab1_description" not in st.session_state:
            st.session_state.tab1_description = f"Expert {business_type} solutions for your home or business. Quality work guaranteed! Contact us today."

        # --- Text Inputs ---
        phone_number = st.text_input(
            "Phone Number", 
            value=st.session_state.tab1_phone, 
            key="tab1_phone"
        )
        st.session_state.tab1_phone = phone_number

        headline = st.text_input(
            "Headline", 
            value=st.session_state.tab1_headline, 
            key="tab1_headline"
        )
        st.session_state.tab1_headline = headline

        description = st.text_area(
            "Description", 
            value=st.session_state.tab1_description, 
            key="tab1_description"
        )
        st.session_state.tab1_description = description

        # --- AI Suggest Button ---
        if st.button("💡 Suggest AI Text", key="tab1_ai_suggest"):
            if business_type:
                with st.spinner("Generating AI copy..."):
                    ai_result = generate_ai_copy(business_type)  # Your AI function
                    ai_headline = ai_result.get("headline", "")
                    ai_description_text = ai_result.get("description", "")
                    ai_hashtags = " ".join(ai_result.get("hashtags", []))
                    ai_description = f"{ai_description_text}\n{ai_hashtags}"

                    # Update session state
                    st.session_state.tab1_headline = ai_headline
                    st.session_state.tab1_description = ai_description

                    st.success("✅ AI suggestion generated!")
                    st.write("**Headline:**", ai_headline)
                    st.write("**Description + Hashtags:**", ai_description)
            else:
                st.warning("⚠️ Select a business type first.")

        # --- Generate Graphic Button ---
        if st.button("Generate Graphic", type="primary", key="tab1_generate_graphic"):
            if headline and description and phone_number:
                # Extract hashtags if any
                hashtags_list = [tag for tag in description.split() if tag.startswith("#")]

                # Generate image with hashtags
                image = create_social_media_graphic(
                    template_type, 
                    business_type, 
                    headline, 
                    description, 
                    phone_number, 
                    hashtags_list
                )

                # Save and display
                os.makedirs("output", exist_ok=True)
                image_path = f"output/graphic_{datetime.now().strftime('%H%M%S')}.png"
                image.save(image_path)

                st.image(image_path, use_column_width=True, caption="Your Professional Social Media Graphic")
                with open(image_path, "rb") as file:
                    st.download_button(
                        "📥 Download Graphic", 
                        file, 
                        file_name=f"{business_type}_social_media_post.png", 
                        mime="image/png",
                        key="tab1_download_btn"
                    )
            else:
                st.warning("⚠️ Please fill in all fields before generating.")


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
    
    st.download_button(
        label="📥 Download Content Calendar",
        data=json.dumps(content_ideas, indent=2),
        file_name="content_calendar.json",
        mime="application/json",
        key="tab2_download_calendar"
    )


st.success("✨ Ready to generate professional social media graphics!")
