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

# ========== BACKGROUND SYSTEM ==========
# Simple local background system (FREE & RELIABLE)
BACKGROUND_CACHE = {
    "Plumbing": [
        "backgrounds/plumbing_bg1.jpg"
    ],
    "Cleaning": [
        "backgrounds/cleaning_bg1.jpg"
    ],
    "HVAC": [
        "backgrounds/hvac_bg1.jpg"
    ],
    "Electrical": [
        "backgrounds/electrical_bg1.jpg"
    ],
    "Landscaping": [
        "backgrounds/landscaping_bg1.jpg"
    ]
}

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
    
    try:
        image = Image.open(background_path)
        return image.resize((1080, 1080))
    except Exception as e:
        # If local file fails, use fallback background
        return create_fallback_background(business_type)

# ========== MAIN GRAPHIC FUNCTION ==========
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