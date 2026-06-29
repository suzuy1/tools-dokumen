import os
import subprocess
import io
from PIL import Image
import fitz  # PyMuPDF
from pypdf import PdfReader, PdfWriter

# Fungsi bantuan untuk membuat preview semua halaman PDF
def generate_pdf_preview(pdf_path, max_pages=30):
    preview_images = []
    try:
        if os.path.exists(pdf_path):
            doc = fitz.open(pdf_path)
            for i in range(min(len(doc), max_pages)):
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                preview_images.append(img)
    except Exception as e:
        print(f"Gagal memuat preview PDF: {e}")
    return preview_images

# 1. KOMPRES PDF
def kompres_pdf(input_file, tingkat_kompresi):
    if input_file is None: 
        return None, "Unggah file PDF terlebih dahulu.", []
    
    input_path = input_file.name
    output_path = "hasil_kompresi.pdf"
    
    kualitas_map = {
        "Sangat Kecil (Resolusi Layar/Web)": '/screen',
        "Kecil (Kualitas Ebook)": '/ebook',
        "Sedang (Kualitas Printer)": '/printer',
        "Bagus (Kualitas Prepress)": '/prepress'
    }
    
    perintah_gs = [
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", 
        f"-dPDFSETTINGS={kualitas_map[tingkat_kompresi]}", 
        "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-sOutputFile={output_path}", 
        input_path
    ]
    
    try:
        subprocess.run(perintah_gs, check=True)
        preview_images = generate_pdf_preview(output_path, max_pages=30)
        ukuran_awal = os.path.getsize(input_path) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        return output_path, f"✅ Sukses!\nUkuran: {ukuran_awal:.2f} MB ➡️ {ukuran_akhir:.2f} MB", preview_images
    except Exception as e: 
        return None, f"❌ Error: {str(e)}", []

# 2. GABUNG PDF (DENGAN PREVIEW)
def gabung_pdf(files):
    if not files: 
        return None, "Silakan pilih minimal 2 file PDF.", []
    if len(files) < 2: 
        return None, "Pilih minimal 2 file untuk digabungkan!", []
    
    output_path = "PDF_Gabungan_Selesai.pdf"
    writer = PdfWriter()
    
    try:
        for file in files:
            writer.append(file.name)
            
        with open(output_path, "wb") as f:
            writer.write(f)
            
        # Generate preview dari file hasil gabungan
        preview_images = generate_pdf_preview(output_path, max_pages=30)
        return output_path, f"✅ Berhasil menggabungkan {len(files)} file PDF!", preview_images
    except Exception as e:
        return None, f"❌ Gagal menggabungkan: {str(e)}", []

# 3. PISAH PDF (DENGAN PREVIEW)
def pisah_pdf(input_file, rentang_halaman):
    if input_file is None: 
        return None, "Unggah file PDF terlebih dahulu.", []
    if not rentang_halaman: 
        return None, "Masukkan rentang halaman (contoh: 1-3).", []
    
    output_path = "PDF_Potongan_Selesai.pdf"
    try:
        reader = PdfReader(input_file.name)
        writer = PdfWriter()
        
        parts = rentang_halaman.split('-')
        start_page = int(parts[0].strip()) - 1
        end_page = int(parts[1].strip())
        
        if start_page < 0 or end_page > len(reader.pages) or start_page >= end_page:
            return None, f"❌ Rentang tidak valid. File ini memiliki {len(reader.pages)} halaman.", []
            
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])
            
        with open(output_path, "wb") as f:
            writer.write(f)
            
        # Generate preview dari potongan PDF yang baru dibuat
        preview_images = generate_pdf_preview(output_path, max_pages=30)
        return output_path, f"✅ Berhasil memotong halaman {rentang_halaman} ({end_page - start_page} halaman).", preview_images
    except Exception:
        return None, f"❌ Format tidak sesuai (Gunakan format: Angka-Angka, misal 1-5)", []