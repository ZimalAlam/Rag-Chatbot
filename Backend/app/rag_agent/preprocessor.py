
import os
import re
from pathlib import Path


def clean_text(text: str) -> str:
    """Basic RAG-friendly text cleaning"""

    # Normalize line breaks
    text = text.replace("\r", "\n")

    # Remove non-ascii characters (keeps numbers and punctuation)
    text = text.encode("ascii", errors="ignore").decode()

    # Lowercase
    text = text.lower()

    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove too many newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Strip edges
    text = text.strip()

    return text


def preprocess_extracted_text(input_folder: str, output_folder: str):
    """
    Reads extracted_pdfs structure and writes cleaned text
    into processed_texts folder with same structure.
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    for pdf_folder in input_path.iterdir():
        if pdf_folder.is_dir():
            print(f"Processing folder: {pdf_folder.name}")

            # Create corresponding output folder
            out_pdf_folder = output_path / pdf_folder.name
            out_pdf_folder.mkdir(exist_ok=True)

            # Loop page files
            for page_file in pdf_folder.glob("*.txt"):
                with open(page_file, "r", encoding="utf-8") as f:
                    raw_text = f.read()

                cleaned = clean_text(raw_text)

                out_file = out_pdf_folder / page_file.name
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(cleaned)

            print(f"Finished {pdf_folder.name}\n")


# ----------------------
# Main for testing
# ----------------------
if __name__ == "__main__":
    extracted_folder = "extracted_pdfs"
    processed_folder = "processed_texts"

    os.makedirs(processed_folder, exist_ok=True)

    print("Preprocessing extracted texts...")
    preprocess_extracted_text(extracted_folder, processed_folder)
    print("Done!")
