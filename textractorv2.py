########### PYTHON
# Script Title: PDFTextractor v2
# Script Description: Recursively finds all PDFs at any depth under a given root folder, skips files with existing markdowns, and outputs each extracted text as `.md` into a `textracted/` subfolder of its first-level parent directory. Modularized for clarity and extensibility.
# Script Author: myPyAI + Naveen Srivatsav
# Last Updated: 20250501
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
    Big-picture: Recursively identify all PDF files in the specified folder and its subdirectories.
    Inputs:  folder (Path) - The directory to search for PDFs.
    Outputs: pdf_files (List[Path]) - List of PDF file paths found in the folder.
    Role: Prepares the list of files for downstream text extraction.
    """
    # Recursively find all PDFs in folder and subdirectories
    return [f for f in folder.rglob("*") if f.suffix.lower() == ".pdf" and f.is_file()]

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

def process_pdfs_in_folder(folder: Path) -> None:
    """
    Big-picture: For each PDF (in any subdirectory), skip if markdown exists, otherwise extract text and save into the `textracted/` folder of its first-level parent directory.
    Inputs:  folder (Path) - Root directory to watch recursively for PDFs.
    Outputs: None
    Role: Coordinates the workflow: listing, extracting, skipping existing, saving, and user feedback.
    """
    pdf_files = get_pdf_files(folder)
    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return
    for pdf_file in pdf_files:
        # Determine first-level output directory
        rel = pdf_file.relative_to(folder)
        parts = rel.parts
        if len(parts) > 1:
            top_dir = parts[0]
            out_dir = folder / top_dir / "textracted"
        else:
            out_dir = folder / "textracted"
        os.makedirs(out_dir, exist_ok=True)
        md_filename = pdf_file.stem + ".md"
        md_path = out_dir / md_filename
        if md_path.exists():
            print(f"Skipping '{pdf_file.name}' as markdown already exists at '{md_path.relative_to(folder)}'")
            continue
        try:
            text = extract_text_from_pdf(pdf_file)
            save_text_to_markdown(text, md_path)
            print(f"Extracted text from '{pdf_file.name}' to '{md_path.relative_to(folder)}'")
        except Exception as e:
            print(f"Failed to extract '{pdf_file.name}': {e}")

def main():
    """
    Big-picture: Prompt for a root folder, validate it, then recursively find PDFs and save markdowns into per-first-level `textracted/` directories, skipping existing outputs.
    Steps:
      1. Prompt the user for a root folder containing PDFs.
      2. Validate the folder path.
      3. Recursively process all PDFs: extract text, skip existing markdowns, and save into each subfolder's `textracted/`.
    Rationale: Automate bulk PDF-to-Markdown conversion without manual subdirectory specification.
    """
    folder_path = input("Enter the path to the folder containing PDFs: ").strip()
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(f"Error: The path '{folder_path}' does not exist or is not a directory.")
        return
    process_pdfs_in_folder(folder)

if __name__ == "__main__":
    main()
