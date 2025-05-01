########### PYTHON
# Script Title: PDF Folder Textractor
# Script Description: Extracts text from all PDF files in a user-specified folder and saves each as a corresponding markdown file in a subdirectory. Modularized for clarity and extensibility, with robust documentation.
# Script Author: myPyAI + Naveen Srivatsav
# Last Updated: 20250430
# """tla ---- MODULE textract ---- EXTENDS Sequences, FileSystem
# VARIABLES folder, pdf_files, text_outputs, output_dir
# Init == 
#     folder = user_input /\ 
#     pdf_files = ListPDFs(folder) /\ 
#     text_outputs = << >> /\ 
#     output_dir = folder/"textracted"
# Next == 
#     \E f \in pdf_files: 
#         text_outputs' = Append(text_outputs, Extract(f)) /\ 
#         Save(text_outputs', output_dir)
# Success == 
#     \A f \in pdf_files: MarkdownExists(f, output_dir)
# ----"""
###########

# To run: pip install pymupdf
# Standard libraries: os, pathlib
# Third-party: fitz (PyMuPDF) for robust PDF parsing and text extraction.

import os
from pathlib import Path
import fitz
from typing import List

def get_pdf_files(folder: Path) -> List[Path]:
    """
    Big-picture: Identify all PDF files in the specified folder.
    Inputs:  folder (Path) - The directory to search for PDFs.
    Outputs: pdf_files (List[Path]) - List of PDF file paths found in the folder.
    Role: Prepares the list of files for downstream text extraction.
    """
    return [f for f in folder.iterdir() if f.suffix.lower() == ".pdf" and f.is_file()]

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Big-picture: Extract all text from a PDF file.
    Inputs:  pdf_path (Path) - Path to the PDF file.
    Outputs: text (str) - The extracted text content from the PDF.
    Role: Converts the PDF's content into plain text for further processing or saving.
    """
    doc = fitz.open(str(pdf_path))
    return "".join(page.get_text() for page in doc)

def save_text_to_markdown(text: str, output_path: Path) -> None:
    """
    Big-picture: Save extracted text to a markdown file at the specified path.
    Inputs:  text (str) - The text to save; output_path (Path) - Where to save the file.
    Outputs: None
    Role: Persists the extracted text for user access and further use.
    """
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(text)

def process_pdfs_in_folder(folder: Path, output_dir: Path) -> None:
    """
    Big-picture: Orchestrate extraction and saving of text from all PDFs in the folder.
    Inputs:  folder (Path) - Directory containing PDFs; output_dir (Path) - Where markdowns are saved.
    Outputs: None
    Role: Coordinates the workflow: listing, extracting, saving, and user feedback.
    """
    pdf_files = get_pdf_files(folder)
    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return
    for pdf_file in pdf_files:
        md_filename = pdf_file.stem + ".md"
        md_path = output_dir / md_filename
        if md_path.exists():
            print(f"Skipping '{pdf_file.name}' as markdown already exists.")
            continue
        try:
            text = extract_text_from_pdf(pdf_file)
            save_text_to_markdown(text, md_path)
            print(f"Extracted text from '{pdf_file.name}' to '{md_path.relative_to(folder)}'")
        except Exception as e:
            print(f"Failed to extract '{pdf_file.name}': {e}")

def main():
    """
    Big-picture:
    1. Prompt the user for a folder containing PDFs.
    2. Validate the folder path.
    3. Create an output directory for markdown files.
    4. Process all PDFs: extract text, save as markdown, and report results.
    Rationale: Modularizes the workflow for clarity, testability, and future extension (e.g., batch processing, format options).
    """
    folder_path = input("Enter the path to the folder containing PDFs: ").strip()
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(f"Error: The path '{folder_path}' does not exist or is not a directory.")
        return
    output_dir = folder / "textracted"
    os.makedirs(output_dir, exist_ok=True)
    process_pdfs_in_folder(folder, output_dir)

if __name__ == "__main__":
    main()
