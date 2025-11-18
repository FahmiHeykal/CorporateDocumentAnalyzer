from docx import Document

# Ganti dengan path file docx kamu
file_path = r"C:\Users\fahmi\AppData\Local\Temp\corporate_docs\784fbfdc-631c-4baa-abe3-d1f68d63b34c.docx"

try:
    doc = Document(file_path)
    full_text = []

    for para in doc.paragraphs:
        if para.text.strip():  # hanya ambil paragraf yang tidak kosong
            full_text.append(para.text)

    if full_text:
        print("Berhasil ekstrak teks! Berikut contoh:")
        print("\n".join(full_text[:10]))  # tampilkan 10 paragraf pertama
    else:
        print("File tidak berisi teks yang bisa diekstrak.")
except Exception as e:
    print(f"Gagal ekstrak teks: {e}")
