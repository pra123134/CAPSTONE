#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install streamlit google-generativeai PyPDF2 Pillow')
import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
from PIL import Image
import io

# Configure Gemini API
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_2.0FLASH"  # Replace with your API key or use os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')  # Use appropriate multimodal model

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to generate recipe using Gemini API
def generate_recipe(user_input, image=None, pdf_text=None):
    prompt = f"""
    You are an expert chef. Based on the following inputs, generate a detailed recipe:
    - User Input: {user_input}
    - PDF Content (if provided): {pdf_text if pdf_text else 'None'}
    Provide a recipe that includes:
    - Ingredients list
    - Step-by-step instructions
    - Cooking time and serving size
    - Any dietary considerations mentioned in the input
    """
    
    if image:
        # Convert image to a format compatible with Gemini API
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_data = img_byte_arr.getvalue()
        response = model.generate_content([prompt, {"mime_type": "image/png", "data": img_data}])
    else:
        response = model.generate_content(prompt)
    
    return response.text

# Streamlit App
def main():
    st.title("AI Chef Recipe Generator")
    st.write("Generate recipes based on your preferences, images, or PDF documents!")

    # User Input Section
    st.header("Step 1: Enter Your Preferences")
    user_input = st.text_area(
        "Enter your dietary preferences, cuisine type, or ingredients you have (e.g., 'vegan Italian with tomatoes')",
        height=150
    )

    # Image Upload Section
    st.header("Step 2: Upload an Image (Optional)")
    uploaded_image = st.file_uploader("Upload an image of ingredients or a dish", type=["jpg", "png", "jpeg"])
    image = None
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # PDF Upload Section
    st.header("Step 3: Upload a PDF (Optional)")
    uploaded_pdf = st.file_uploader("Upload a PDF with additional recipe details or requirements", type=["pdf"])
    pdf_text = None
    if uploaded_pdf:
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        st.write("Extracted PDF Text:")
        st.text_area("PDF Content", pdf_text, height=200)

    # Generate Recipe Button
    if st.button("Generate Recipe"):
        if not user_input and not image and not pdf_text:
            st.error("Please provide at least one input (text, image, or PDF).")
        else:
            with st.spinner("Generating your recipe..."):
                recipe = generate_recipe(user_input, image, pdf_text)
                st.subheader("Generated Recipe")
                st.markdown(recipe)

if __name__ == "__main__":
    main()


# In[ ]:




