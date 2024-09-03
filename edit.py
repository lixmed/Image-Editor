import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont

# Set the app title and custom styles
st.set_page_config(page_title="Artistic Image Editor", layout="wide")

# Custom HTML/CSS for styling
st.markdown("""
<style>
/* Page Background */
.reportview-container {
    background: linear-gradient(135deg, #fce4ec, #f8bbd0); /* Gradient pink background */
    font-family: 'Arial', sans-serif;
}


/* Title and Subtitle */
.title {
    font-size: 4rem;
    color: #d81b60; /* Vibrant pink */
    text-align: center;
    margin: 3rem 0;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Shadow to enhance readability */
}

.subtitle {
    font-size: 2rem;
    color: #c2185b; /* Slightly darker pink */
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 500;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2); /* Shadow to enhance readability */
}

/* Welcome Message */
.welcome-message {
    font-size: 1.5rem;
    color: #d81b60; /* Vibrant pink */
    text-align: center;
    margin: 2rem 0;
    font-weight: 500;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2); /* Shadow to enhance readability */
}

/* Buttons */
.button {
    border: 2px solid #d81b60; /* Pink border */
    border-radius: 12px; /* Rounded corners */
    background: linear-gradient(145deg, #e91e63, #d81b60); /* Gradient background */
    color: #fff;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    font-size: 1rem;
    margin: 0.5rem;
    transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
}

.button:hover {
    background: linear-gradient(145deg, #c2185b, #880e4f); /* Darker gradient */
    border: 2px solid #880e4f; /* Darker pink border */
}

.button:active {
    background: linear-gradient(145deg, #880e4f, #560027); /* Even darker gradient */
    transform: scale(0.98);
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
}

/* Text Input Borders */
.stTextInput input {
    border: 2px solid #d81b60; /* Pink border */
    border-radius: 8px; /* Rounded corners */
    padding: 0.5rem;
    transition: border-color 0.3s ease;
}

.stTextInput input:focus {
    border-color: #c2185b; /* Darker pink on focus */
    outline: none;
}

/* Sidebar Styling */
.sidebar .sidebar-content {
    border: 2px solid #d81b60; /* Pink border */
    border-radius: 15px; /* Rounded corners */
    padding: 2rem;
    background-color: #f8bbd0; /* Light pink background */
}

/* Keyframe Animation */
@keyframes pulse {
    0% {
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
    }
    50% {
        text-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5);
    }
    100% {
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
    }
}
</style>

""", unsafe_allow_html=True)

# Add HTML for top and bottom bars
st.markdown('<div class="top-bar">Welcome to Artistic Image Editor made by Ahmed</div>', unsafe_allow_html=True)
st.markdown('<div class="bottom-bar">© 2024 Artistic Image Editor. All rights reserved.</div>', unsafe_allow_html=True)

# Adjust content padding to account for fixed bars
st.markdown('<div class="content">', unsafe_allow_html=True)

# Title and subtitle of the app
st.markdown('<h1 class="title">Artistic Image Editor</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">Enhance and Transform Your Photos</h2>', unsafe_allow_html=True)

# Initialize or reset the session state
def initialize_image(uploaded_file):
    if 'image' not in st.session_state:
        st.session_state.image = Image.open(uploaded_file)

# Apply selected filter to the image
def apply_filter(image, filter_type):
    if filter_type == "Blur":
        return image.filter(ImageFilter.BLUR)
    elif filter_type == "Contour":
        return image.filter(ImageFilter.CONTOUR)
    elif filter_type == "Detail":
        return image.filter(ImageFilter.DETAIL)
    elif filter_type == "Sharpen":
        return image.filter(ImageFilter.SHARPEN)
    elif filter_type == "Enhance Contrast":
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2)
    return image

# Apply selected crop to the image
def apply_crop(image, crop_type):
    width, height = image.size
    if crop_type == "Square":
        min_side = min(width, height)
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        return image.crop((left, top, left + min_side, top + min_side))
    elif crop_type == "Circle":
        min_side = min(width, height)
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        mask = Image.new('L', (min_side, min_side), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, min_side, min_side), fill=255)
        image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        image.putalpha(mask)
        return image
    elif crop_type == "Rectangle":
        left = width * 0.1
        top = height * 0.1
        right = width * 0.9
        bottom = height * 0.9
        return image.crop((left, top, right, bottom))
    return image

# Apply rotation to the image
def apply_rotation(image, angle):
    return image.rotate(angle, expand=True)

# Add text to the image
def add_text_to_image(image, text, font_size, text_color, x_position, y_position):
    image = image.convert("RGBA")
    txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(txt)
    d.text((x_position, y_position), text, fill=text_color, font=font)
    return Image.alpha_composite(image, txt)

# Display uploaded image
def display_image(image, caption):
    st.image(image, caption=caption, use_column_width=True)

# Reset the session state image
def reset_image(uploaded_file):
    st.session_state.image = Image.open(uploaded_file)

# Main code
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    initialize_image(uploaded_file)
    display_image(st.session_state.image, 'Uploaded Image')

    # Filters
    st.sidebar.title("Filters")
    filter_type = st.sidebar.radio("Select a filter to apply:", ["None", "Blur", "Contour", "Detail", "Sharpen", "Enhance Contrast"])
    if filter_type != "None":
        st.session_state.image = apply_filter(st.session_state.image, filter_type)
        display_image(st.session_state.image, f'{filter_type} Applied')

    # Crop
    st.sidebar.title("Crop")
    crop_type = st.sidebar.radio("Select a shape to crop:", ["None", "Square", "Circle", "Rectangle"])
    if crop_type != "None":
        st.session_state.image = apply_crop(st.session_state.image, crop_type)
        display_image(st.session_state.image, f'{crop_type} Crop Applied')

    # Rotation
    st.sidebar.title("Rotate")
    rotation_angle = st.sidebar.slider("Rotate Image by Degrees:", min_value=-180, max_value=180, value=0)
    if rotation_angle != 0:
        st.session_state.image = apply_rotation(st.session_state.image, rotation_angle)
        display_image(st.session_state.image, f'Rotated by {rotation_angle} Degrees')

    # Add Text
    st.sidebar.title("Add Text")
    add_text = st.sidebar.text_input("Enter text to add:")
    font_size = st.sidebar.slider("Select font size:", min_value=10, max_value=100, value=30)
    text_color = st.sidebar.color_picker("Pick a text color:", "#FFFFFF")
    x_position = st.sidebar.slider("X position:", min_value=0, max_value=st.session_state.image.width, value=50)
    y_position = st.sidebar.slider("Y position:", min_value=0, max_value=st.session_state.image.height, value=50)
    if add_text:
        st.session_state.image = add_text_to_image(st.session_state.image, add_text, font_size, text_color, x_position, y_position)
        display_image(st.session_state.image, "Text Added")

    # Save the image
    st.sidebar.title("Save Image")
    if st.sidebar.button("Save Image", key="save_button"):
        st.session_state.image.save("edited_image.png")
        st.sidebar.success("Image saved as edited_image.png")

    # Reset the image
    if st.sidebar.button("Reset Image", key="reset_button"):
        reset_image(uploaded_file)
        st.session_state.image = Image.open(uploaded_file)
        st.sidebar.success("Image reset to original.")
        display_image(st.session_state.image, 'Reset to Original Image')
