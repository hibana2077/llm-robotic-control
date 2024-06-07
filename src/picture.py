import streamlit as st
from PIL import Image
import numpy as np

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Check the shape of img_array:
    # Should output shape: (height, width, channels)
    st.write(img_array.shape)

    if st.button("Save picture"):
        st.image(img_array, caption="Your picture", use_column_width=True)