import streamlit as st
import random
import numpy as np
import tempfile
import cv2
from PIL import Image
from src.main import blend_images
def load_image(file):
    image = Image.open(file)
    return np.array(image)

st.title("Image Patchwork Tool")

uploaded_images = st.file_uploader(
    "Upload multiple images", type=["png", "jpg", "jpeg","webp"], accept_multiple_files=True
)

ratio_mode = st.radio("Ratio input method", ["Manual", "Random"])

if ratio_mode == "Manual":
    ratio_input = st.text_input("Blend ratios (comma-separated)", "1,1")
else:
    ratio_input = None

block_size_input = st.text_input(
    "Block size (e.g., 16 or 16,32 or 8,32,8,32)", "16"
)

if st.button("Start") and uploaded_images:
    images = [load_image(f) for f in uploaded_images]

    h, w = images[0].shape[:2]
    images = [cv2.resize(img, (w, h)) for img in images]

    try:
        if ratio_mode == "Manual":
            ratios = list(map(float, ratio_input.strip().split(",")))
        else:
            ratios = [random.random() for _ in range(len(images))]

        block_parts = list(map(int, block_size_input.strip().split(",")))
        if len(block_parts) == 1:
            block_size = block_parts[0]
        elif len(block_parts) == 2 or len(block_parts) == 4:
            block_size = tuple(block_parts)
        else:
            st.error("Invalid block size format.")

        result = blend_images(
            images, ratios, block_size=block_size
        )
        st.image(result, caption="Patchworked Image", channels="RGB")

        result_img = Image.fromarray(result)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            result_img.save(tmpfile.name)
            st.download_button("Download",open(tmpfile.name, "rb"),file_name="blended.png")

    except Exception as e:
        st.error(f"An error occurred: {e}")