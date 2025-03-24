import streamlit as st
import google.generativeai as genai
import pdfplumber
import base64
import io
from PIL import Image

# ✅ Configure API Key securely
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

# ✅ Extract text from PDF (better support for scanned PDFs)
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip() or "No text extracted. The PDF might be image-based."

# ✅ Convert image to base64 for Gemini processing
def convert_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return img_data

# ✅ Generate AI Recipe Response
def generate_recipe(user_input, image=None, pdf_text=None):
    prompt = f"""
    You are a world-class chef. Based on the following inputs, create a professional recipe:
    - User Preferences: {user_input}
    - PDF Content (if provided): {pdf_text if pdf_text else 'None'}
    Include:
    - Ingredients list
    - Step-by-step instructions
    - Cooking time and servings
    - Dietary considerations
    """
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    try:
        if image:
            img_data = convert_image(image)
            response = model.generate_content([prompt, {"mime_type": "image/png", "data": img_data}], stream=True)
        else:
            response = model.generate_content(prompt, stream=True)
        return "".join(chunk.text for chunk in response)
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}\nPlease try again later."

# ✅ Streamlit App
def main():
    st.title("🍽️ AI Chef Recipe Generator")
    st.write("Create unique recipes based on ingredients, cuisine type, or dietary needs!")
    
    # ✅ User Input
    st.header("Step 1: Enter Your Preferences")
    user_input = st.text_area("Describe what you're looking for (e.g., 'vegan Italian pasta with mushrooms')", height=150)
    
    # ✅ Dietary Preferences
    dietary_options = ["None", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Paleo"]
    dietary_choice = st.selectbox("Select Dietary Preference (Optional)", dietary_options)
    if dietary_choice != "None":
        user_input += f" (Dietary preference: {dietary_choice})"
    
    # ✅ Image Upload
    st.header("Step 2: Upload an Image (Optional)")
    uploaded_image = st.file_uploader("Upload an image of ingredients or a dish", type=["jpg", "png", "jpeg"])
    image = Image.open(uploaded_image) if uploaded_image else None
    if image:
        st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # ✅ PDF Upload
    st.header("Step 3: Upload a PDF (Optional)")
    uploaded_pdf = st.file_uploader("Upload a PDF with recipe details or ingredient lists", type=["pdf"])
    pdf_text = extract_text_from_pdf(uploaded_pdf) if uploaded_pdf else None
    if pdf_text:
        st.text_area("Extracted PDF Content", pdf_text, height=200)
    
    # ✅ Generate Recipe Button
    if st.button("🍳 Generate Recipe"):
        if not user_input and not image and not pdf_text:
            st.error("⚠️ Please provide at least one input (text, image, or PDF).")
        else:
            with st.spinner("Generating your recipe... 🍽️"):
                recipe = generate_recipe(user_input, image, pdf_text)
                st.subheader("✨ Generated Recipe")
                st.markdown(recipe)

if __name__ == "__main__":
    main()
