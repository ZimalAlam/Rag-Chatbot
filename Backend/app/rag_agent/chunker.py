import os
from pathlib import Path

MIN_WORDS_PER_CHUNK = 120
OVERLAP_WORDS = 50


def split_into_paragraphs(text: str):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def create_chunks_from_text(text: str):
    paragraphs = split_into_paragraphs(text)
    chunks = []
    buffer_words = []

    for para in paragraphs:
        words = para.split()

        if len(words) >= MIN_WORDS_PER_CHUNK:
            if buffer_words:
                chunks.append(buffer_words)
                buffer_words = []

            start = 0
            while start < len(words):
                end = start + MIN_WORDS_PER_CHUNK
                chunk = words[start:end]
                chunks.append(chunk)
                start += MIN_WORDS_PER_CHUNK - OVERLAP_WORDS
            continue

        if len(buffer_words) + len(words) < MIN_WORDS_PER_CHUNK:
            buffer_words.extend(words)
        else:
            chunks.append(buffer_words)
            buffer_words = words.copy()

    if buffer_words:
        chunks.append(buffer_words)

    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            final_chunks.append(chunk)
        else:
            overlap = final_chunks[-1][-OVERLAP_WORDS:]
            final_chunks.append(overlap + chunk)

    return [" ".join(c).strip() for c in final_chunks if c]


def chunk_processed_texts(input_folder: str, output_folder: str):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    for pdf_folder in sorted(input_path.iterdir()):
        if pdf_folder.is_dir():
            print("\n==============================")
            print(f"📂 Processing PDF folder: {pdf_folder.name}")
            print("==============================")

            out_pdf_folder = output_path / pdf_folder.name
            out_pdf_folder.mkdir(exist_ok=True)

            chunk_counter = 1

            for page_file in sorted(pdf_folder.glob("*.txt")):
                print(f"\n📄 Reading page file: {page_file}")
                with open(page_file, "r", encoding="utf-8") as f:
                    text = f.read()

                print(f"🔍 First 80 chars: {text[:80].replace(chr(10), ' ')}")

                chunks = create_chunks_from_text(text)
                print(f"🧠 Chunks created from this page: {len(chunks)}")

                for chunk in chunks:
                    if not chunk.strip():
                        print("⚠️ Skipped empty chunk")
                        continue

                    chunk_file = out_pdf_folder / f"chunk_{chunk_counter}.txt"
                    print(f"💾 Saving chunk {chunk_counter} → {chunk_file}")

                    with open(chunk_file, "w", encoding="utf-8") as f:
                        f.write(chunk)

                    chunk_counter += 1

            print(f"\n✅ Total chunks saved for {pdf_folder.name}: {chunk_counter-1}")


if __name__ == "__main__":
    processed_folder = "processed_texts"
    chunked_folder = "chunked_texts"

    os.makedirs(chunked_folder, exist_ok=True)

    print("🚀 DEBUG CHUNKING STARTED")
    chunk_processed_texts(processed_folder, chunked_folder)
    print("\n🎉 DONE")
