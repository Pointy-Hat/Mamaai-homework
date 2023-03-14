from pdfminer.high_level import extract_pages


def mine_pdf(file_name):
    chunk_texts = []
    for page_layout in extract_pages(file_name):
        chunk_texts += [
            element.get_text().strip()
            for element in page_layout
            if hasattr(element, "get_text")
        ]
    return chunk_texts
