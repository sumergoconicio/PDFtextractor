import os
from pathlib import Path
import fitz  # PyMuPDF

# Prompt user for folder path
folder_path = input("Enter the path to the folder containing PDFs: ").strip()
folder = Path(folder_path)

if not folder.exists() or not folder.is_dir():
    print(f"Error: The path '{folder_path}' does not exist or is not a directory.")
    exit(1)

# Create output directory
output_dir = folder / "textracted"
os.makedirs(output_dir, exist_ok=True)

# List all PDF files in the folder
pdf_files = [f for f in folder.iterdir() if f.suffix.lower() == ".pdf" and f.is_file()]

if not pdf_files:
    print("No PDF files found in the specified directory.")
    exit(0)

for pdf_file in pdf_files:
    try:
        doc = fitz.open(str(pdf_file))
        text = ""
        for page in doc:
            text += page.get_text()
        # Save to markdown file
        md_filename = pdf_file.stem + ".md"
        md_path = output_dir / md_filename
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(text)
        print(f"Extracted text from '{pdf_file.name}' to '{md_path.relative_to(folder)}'")
    except Exception as e:
        print(f"Failed to extract '{pdf_file.name}': {e}")
