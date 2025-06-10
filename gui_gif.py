import streamlit as st
import tempfile
import random
import numpy as np
from src.glitch_gif import glitch_gif

uploaded_file = st.file_uploader(
    "Upload a GIF file",
    type=["gif"],
    accept_multiple_files=False
    )

temporal_window_str = st.text_input(
    "Number of frames before and after the frame are included in the mix", "1")
try:
    temporal_window = int(temporal_window_str)
    if temporal_window < 0:
        st.error("Number of frames must be integer at least 0.")
        temporal_window = 0
except ValueError:
    st.error("Please enter an integer at least 0 in Numer of frames.")

num_sources = 2 * temporal_window + 1

ratio_mode = st.radio("Ratio input method", ["Manual", "Random", "Centered"])

if ratio_mode == "Manual":
    ratio_input = st.text_input("Blend ratios (comma-separated 2*temporal_window + 1 numbers)", 
                                "1,"*(num_sources -1) + "1" if num_sources > 0 else "1"
                                )
else:
    ratio_input = None

block_size_input = st.text_input(
    "Block size (e.g., 1 or 2,4 or 2,4,4,8)", "1")
try:
    block_parts = list(map(int, block_size_input.strip().split(",")))
    if any(p <= 0 for p in block_parts):
        st.error("Block size must be an integer or tuple of integers at least 0.")
except ValueError:
    st.error("Please enter an integer or tuple of integers at least 0 in Block size")

if st.button("Start") and uploaded_file:
    try:

        if ratio_mode == "Manual":
            ratios = list(map(float, ratio_input.strip().split(",")))
        elif ratio_mode == 'Random':
            ratios = np.random.rand(num_sources)
        elif ratio_mode == 'Centered':
            ratios = np.zeros(num_sources)
            for i in range (1, temporal_window + 1):
                ratios[i - 1] = i
                ratios[num_sources - i] = i
            ratios[temporal_window] = temporal_window + 1

        block_size = block_parts if len(block_parts) > 1 else block_parts[0]

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
            tmpfile.write(uploaded_file.read())
            tmpfile_path = tmpfile.name

        result_gif = glitch_gif(
            input_path = tmpfile_path,
            temporal_window=temporal_window,
            mode="Manual",
            ratios=ratios,
            block_size=block_size
        )

        st.image(result_gif.getvalue(), caption="Glitched GIF", use_container_width=True)

        st.download_button(
            "Download",
            data=result_gif.getvalue(),
            file_name="glitched.gif",
            mime="image/gif"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")