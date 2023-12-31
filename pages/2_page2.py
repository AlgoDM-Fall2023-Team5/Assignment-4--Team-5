import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from sentence_transformers import SentenceTransformer
import json  # Add this import

url = "http://127.0.0.1:8000"
path = "C:/Users/shiri/Documents/Assg4ADM/dataset"

image_encoder = SentenceTransformer('clip-ViT-B-32')

st.title("Image Similarity Search")

uploaded_image = st.file_uploader("Choose an image...", type="jpg")

def encode_image(uploaded_image, encoder):
    image_bytes = uploaded_image.read()
    image_pil = Image.open(BytesIO(image_bytes))

    # Encode the image
    image_input = encoder.encode(image_pil, convert_to_tensor=True)
    image_features = image_input.flatten()

    return image_features

if uploaded_image is not None:
    if st.button("Find Similar Images"):
        st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

        # Encode the image
        image_features = encode_image(uploaded_image, image_encoder)

        # Convert the NumPy array to a list
        image_features_list = image_features.tolist()
        st.write(image_features_list)

        # Send the image vector as JSON in the request body
        response = requests.post(f"{url}/image_search", json={"image": image_features_list})
        features = response.json()


        for i in features:
            image_path = path +'/' +i 
            image = Image.open(image_path)
            st.image(image, use_column_width=True)

        st.write(features)
