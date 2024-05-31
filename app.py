import streamlit as st
import os
from pdf2image import convert_from_path
from PIL import Image
from docx import Document

# Function to convert PDF to text
def pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# Function to convert DOCX to text
def docx_to_text(docx_path):
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to convert image to text
def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Streamlit UI
def main():
    st.title("File Converter")

    # File upload
    st.sidebar.header("Upload Files")
    uploaded_file = st.sidebar.file_uploader("Upload a file", type=["pdf", "txt", "docx", "ppt", "png", "jpg"])

    if uploaded_file is not None:
        # Display file details
        st.sidebar.write("File Details:")
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.sidebar.write(file_details)

        # Conversion selection
        conversion_format = st.sidebar.selectbox("Select conversion format", ["pdf", "txt", "docx", "ppt", "png", "jpg"])

        if st.sidebar.button("Convert"):
            # Perform conversion
            if conversion_format == "pdf":
                st.write("Converting PDF file...")
                text = pdf_to_text(uploaded_file)
            elif conversion_format == "txt":
                st.write("Converting TXT file...")
                text = uploaded_file.read().decode("utf-8")
            elif conversion_format == "docx":
                st.write("Converting DOCX file...")
                text = docx_to_text(uploaded_file)
            elif conversion_format == "ppt":
                st.write("Converting PPT file... (not implemented)")
                text = ""
            elif conversion_format == "png" or conversion_format == "jpg":
                st.write("Converting image file... (not implemented)")
                text = ""

            # Display converted text
            if text:
                st.write("Converted Text:")
                st.write(text)

            # Download converted file
            if st.button("Download Converted File"):
                if conversion_format == "txt" or conversion_format == "docx":
                    with open(f"converted_{uploaded_file.name}", "w", encoding="utf-8") as file:
                        file.write(text)
                elif conversion_format == "pdf":
                    images = convert_from_path(uploaded_file.name)
                    for i, image in enumerate(images):
                        image.save(f"converted_{uploaded_file.name}_{i}.jpg", "JPEG")
                elif conversion_format == "ppt":
                    st.write("Download feature for PPT conversion is not implemented yet.")
                elif conversion_format == "png" or conversion_format == "jpg":
                    st.write("Download feature for image conversion is not implemented yet.")
                else:
                    st.write("Invalid conversion format selected.")

if __name__ == "__main__":
    main()
