from pathlib import Path
from backend.app.services.loader import load_document  # Adjust to your function name

UPLOAD_DIR = Path("backend/data/uploads")
# pdf_files = UPLOAD_DIR.glob("*.pdf")
# print(pdf_files)
def test_pdf_loader():

    pdf_files = list(UPLOAD_DIR.glob("*.pdf"))
    # print(f"Total pages/documents: {pdf_files}")

    if not pdf_files:
        print("No PDF files found!")
        return

    for pdf_file in pdf_files:
        print(f"\nTesting: {pdf_file.name}")

        documents = load_document(str(pdf_file),'vikash')

        print(f"Total pages/documents: {len(documents)}")
        for doc in documents:
            print(f"Total pages/documents: {doc.metadata})")

            # for doc in documents:
            #     print("Metadata:", doc.metadata)
            #     print("Extracted content:")
            #     print(doc.page_content[:500])

            # assert len(documents) > 0
            # assert documents[0].page_content.strip() != ""

    print("\nPDF loader test completed successfully!")

if __name__ == "__main__":
    test_pdf_loader()