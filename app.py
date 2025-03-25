import google.generativeai as genai
import PyPDF2
from PIL import Image
import io
#import IPython.display as display
import streamlit as st

# Configure Gemini API
# Configure API Key securely
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-pro')

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
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_data = img_byte_arr.getvalue()
        response = model.generate_content([prompt, {"mime_type": "image/png", "data": img_data}])
    else:
        response = model.generate_content(prompt)

    return response.text

# Function to generate seasonal recipe using Gemini API
def generate_recipe(ingredients, season, cuisine):
    """Generates an innovative recipe idea based on input."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (f"Create an innovative recipe using seasonal ingredients: {season}, "
              f"local specialties: {ingredients}, and in the style of {cuisine} cuisine. "
              "Provide a creative dish name, key ingredients, and a step-by-step preparation method.")

    response = model.generate_content(prompt)
    return response.text.strip() if response else "No recipe generated. Try again."

# Jupyter Notebook/Colab App
def main():
    print("AI Chef Recipe Generator")
    print("Generate recipes based on your preferences, images, or PDF documents!")

    # Input Choice
    print("\nChoose your option to get Reciepe:")
    print("1. Search Reciepe by name")
    print("2. Reciepe from Image ")
    print("3. Reciepe from PDF")
    print("4. Seasonal ingradients Reciepe")
    print("5. Reciepe  from Leftover ingradients")
    choice = input("Enter your choice (1, 2, 3, 4 or 5): ")

    user_input = None
    image = None
    pdf_text = None

    if choice == "1":
        # Text Input
        print("\nStep 1: Enter Your Preferences")
        user_input = input("Enter your dietary preferences, cuisine type, or ingredients you have (e.g., 'vegan Italian with tomatoes'): ")
    elif choice == "2":
        # Image Input
        print("\nStep 2: Upload an Image")
        uploaded_image_path = input("Enter the path to your image file: ")
        try:
            image = Image.open(uploaded_image_path)
            display.display(image)
        except FileNotFoundError:
            print("Image file not found.")
            return
    elif choice == "3":
        # PDF Input
        print("\nStep 3: Upload a PDF")
        uploaded_pdf_path = input("Enter the path to your PDF file: ")
        try:
            with open(uploaded_pdf_path, 'rb') as pdf_file:
                pdf_text = extract_text_from_pdf(pdf_file)
            print("\nExtracted PDF Text:")
            print(pdf_text)
        except FileNotFoundError:
            print("PDF file not found.")
            return
        except PyPDF2.errors.PdfReadError:
            print("Invalid PDF File.")
            return
    elif choice == "4":
        # Get user input (replace with your preferred method)
        season = input("Select the current season (Spring, Summer, Autumn, Winter): ")
        cuisine = input("Preferred cuisine style (e.g., Italian, Indian, Fusion): ")
        ingredients = input("Enter local specialties (comma-separated): ")

        # Generate and print the recipe
        recipe = generate_recipe(ingredients, season, cuisine)
        print("\nAI-Generated Recipe:\n")
        print(recipe)
        return
    elif choice == "5":
        # Text Input
        print("\nStep 1: Enter Leftover ingredients")
        user_input = input("Enter your dietary preferences, cuisine type, and leftover ingredients")
    else:
        print("Invalid choice.")
        return

    # Generate Recipe
    if user_input or image or pdf_text:
        print("\nGenerating your recipe...")
        recipe = generate_recipe(user_input, image, pdf_text)
        print("\nGenerated Recipe:")
        print(recipe)
    else:
        print("\nNo input provided.")

if __name__ == "__main__":
    main()
