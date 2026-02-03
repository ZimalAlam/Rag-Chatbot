import os
from pathlib import Path
from PyPDF2 import PdfReader

def extract_pdfs(input_folder: str, output_folder: str):
    """
    Extracts text from all PDFs in input_folder and saves
    page-wise text files in output_folder/<pdf_name>/pageX.txt
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through all PDFs
    for pdf_file in input_path.glob("*.pdf"):
        print(f"Processing: {pdf_file.name}")
        pdf_reader = PdfReader(str(pdf_file))

        # Create folder for this PDF
        pdf_folder = output_path / pdf_file.stem
        pdf_folder.mkdir(exist_ok=True)

        # Extract each page
        for i, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text() or ""  # fallback empty if no text
            page_file = pdf_folder / f"page{i+1}.txt"
            with open(page_file, "w", encoding="utf-8") as f:
                f.write(page_text)
        print(f"Saved {len(pdf_reader.pages)} pages for {pdf_file.name}\n")


# ----------------------
# Main function for testing
# ----------------------
if __name__ == "__main__":
    # Folder where PDFs are stored for testing
    test_input_folder = "test_pdfs"
    # Folder where extracted txts will go
    test_output_folder = "extracted_pdfs"

    # Create test folders if not exist
    os.makedirs(test_input_folder, exist_ok=True)
    os.makedirs(test_output_folder, exist_ok=True)

    print("Place some PDFs in the 'test_pdfs' folder and run this script.")
    extract_pdfs(test_input_folder, test_output_folder)
    print("Extraction complete!")
