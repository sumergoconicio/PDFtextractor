# PDFtextractor

A simple Python script to batch-extract text from all PDF files in a specified folder and save the extracted text as Markdown files.

## Features
- Extracts text from every PDF in a chosen directory
- Saves extracted text as `.md` files in a `textracted/` subfolder
- Handles errors gracefully and provides clear messages
- Skips PDFs if corresponding markdown already exists to avoid reprocessing

## Requirements
- Python 3.7+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)

## Installation
1. Clone this repository or download the script.
2. Install the required dependencies:
   ```bash
   pip install pymupdf
   ```

## Usage
1. Run the script:
   ```bash
   python textractor.py
   ```
2. When prompted, enter the path to the folder containing your PDF files.
3. The script will:
   - Check the folder exists and contains PDF files
   - Extract text from each PDF
   - Save each PDF's text as a Markdown file in a `textracted/` subfolder next to your PDFs
   - Skip PDFs whose `.md` output already exists

## Output
- For each PDF, a corresponding `.md` file will be created in `textracted/`.
- Example: `document.pdf` → `textracted/document.md`

## Example
```bash
$ python textractor.py
Enter the path to the folder containing PDFs: /path/to/my/pdfs
Extracted text from 'file1.pdf' to 'textracted/file1.md'
Extracted text from 'file2.pdf' to 'textracted/file2.md'
```

## Versions
- **v1 (`textractor.py`)**: Simple version that processes a single folder, extracting PDFs directly within and saving markdowns into a `textracted/` subfolder.
- **v2 (`textractorv2.py`)**: Advanced version that watches a root folder recursively, processes PDFs at any depth, skips files with existing `.md`, and outputs each into its first-level subfolder's `textracted/`.

Recommended: for most use cases, start with **v1** and extend it as needed.

## Troubleshooting
- Ensure you have permission to read the PDF files and write to the output directory.
- If you encounter errors, check that the folder path is correct and that the PDFs are not corrupted.

## License
MIT License
