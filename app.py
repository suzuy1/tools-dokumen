import gradio as gr
import subprocess
import os
import zipfile
import tempfile
import shutil
import io
from PIL import Image
import fitz  # Library PyMuPDF untuk preview PDF
import docx  # Library python-docx untuk preview Word

# ==========================================
# FUNGSI 1: KOMPRES & PREVIEW PDF (SEMUA HALAMAN)
# ==========================================
def kompres_pdf(input_file, tingkat_kompresi):
    if input_file is None:
        return None, "Silakan unggah file PDF terlebih dahulu.", []
    
    if not input_file.name.lower().endswith('.pdf'):
        return None, "Maaf, ini tab khusus PDF. Gunakan tab Word untuk file .docx", []

    input_path = input_file.name
    output_path = "hasil_kompresi.pdf"
    
    kualitas_map = {
        "Sangat Kecil (Resolusi Layar/Web)": '/screen',
        "Kecil (Kualitas Ebook)": '/ebook',
        "Sedang (Kualitas Printer)": '/printer',
        "Bagus (Kualitas Prepress)": '/prepress'
    }
    
    perintah_gs = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={kualitas_map[tingkat_kompresi]}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    try:
        # 1. Jalankan Proses Kompresi
        subprocess.run(perintah_gs, check=True)
        
        # 2. PROSES PREVIEW: Render Semua Halaman ke Galeri
        preview_images = []
        try:
            doc = fitz.open(output_path)
            # Batasi preview max 50 halaman agar server gratis tidak crash
            max_pages = min(len(doc), 50) 
            
            for i in range(max_pages):
                page = doc.load_page(i)
                # Matrix 1.0 cukup untuk preview galeri agar prosesnya cepat
                pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0)) 
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                preview_images.append(img)
        except Exception as e:
            print(f"Gagal memuat preview PDF: {e}")
            preview_images = [] # Kosongkan jika gagal

        # 3. Kalkulasi Ukuran
        ukuran_awal = os.path.getsize(input_path) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        pesan = f"✅ Sukses!\nUkuran Awal: {ukuran_awal:.2f} MB ➡️ Ukuran Akhir: {ukuran_akhir:.2f} MB"
        
        return output_path, pesan, preview_images
    except Exception as e:
        return None, f"❌ Terjadi kesalahan: {str(e)}", []

# ==========================================
# FUNGSI 2: KOMPRES & PREVIEW WORD (.DOCX)
# ==========================================
def kompres_word(input_file, tingkat_kompresi):
    if input_file is None:
        return None, "Silakan unggah file Word (.docx) terlebih dahulu.", None
    
    if not input_file.name.lower().endswith('.docx'):
        return None, "Maaf, ini tab khusus Word. Gunakan tab PDF untuk file .pdf", None

    input_path = input_file.name
    output_path = "hasil_kompresi.docx"
    
    kualitas_map = {
        "Sangat Agresif (Ukuran Paling Kecil)": (40, 800),
        "Standar (Rekomendasi)": (60, 1200),
        "Ringan (Kualitas Gambar Terjaga)": (80, 1600)
    }
    
    kualitas_jpeg, max_lebar = kualitas_map[tingkat_kompresi]
    temp_dir = tempfile.mkdtemp()
    gambar_diproses = 0
    
    try:
        # Proses Kompresi Gambar dalam Word
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
        media_path = os.path.join(temp_dir, 'word', 'media')
        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                file_path = os.path.join(media_path, filename)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = Image.open(file_path)
                        if img.width > max_lebar:
                            rasio = max_lebar / img.width
                            tinggi_baru = int(img.height * rasio)
                            img = img.resize((max_lebar, tinggi_baru), Image.Resampling.LANCZOS)
                        
                        if filename.lower().endswith(('.jpg', '.jpeg')):
                            img.save(file_path, "JPEG", optimize=True, quality=kualitas_jpeg)
                        elif filename.lower().endswith('.png'):
                            img.save(file_path, "PNG", optimize=True)
                        gambar_diproses += 1
                    except Exception:
                        pass

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx_zip:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    docx_zip.write(full_path, rel_path)
                    
        # PROSES PREVIEW: Ekstrak Teks dari Word
        try:
            doc_obj = docx.Document(output_path)
            teks_terkumpul = []
            for p in doc_obj.paragraphs:
                if p.text.strip(): # Abaikan paragraf kosong
                    teks_terkumpul.append(p.text.strip())
                if len(teks_terkumpul) >= 5: # Ambil 5 paragraf pertama
                    break
            preview_teks = "\n\n".join(teks_terkumpul)
            if not preview_teks:
                preview_teks = "[Dokumen ini hanya berisi gambar/tabel, tidak ada teks biasa]"
        except Exception:
            preview_teks = "[Tidak dapat memuat preview teks]"
                    
        ukuran_awal = os.path.getsize(input_path) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        pesan = (f"✅ Sukses! {gambar_diproses} gambar dikompres.\n"
                 f"Ukuran Awal: {ukuran_awal:.2f} MB ➡️ Ukuran Akhir: {ukuran_akhir:.2f} MB")
                 
        return output_path, pesan, preview_teks
        
    except Exception as e:
        return None, f"❌ Terjadi kesalahan: {str(e)}", None
    finally:
        shutil.rmtree(temp_dir)

# ==========================================
# ANTARMUKA PENGGUNA (UI) DENGAN PREVIEW
# ==========================================
with gr.Blocks(title="Alat Kompresi Gratis", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🗜️ Alat Kompresi Dokumen Super (100% Gratis)")
    gr.Markdown("Pilih jenis dokumen yang ingin Anda kompres pada tab di bawah ini. Aman, cepat, dan tanpa batasan!")
    
    with gr.Tabs():
        # TAB 1: PDF
        with gr.TabItem("📕 Kompres PDF"):
            with gr.Row():
                with gr.Column():
                    pdf_input = gr.File(label="Unggah File PDF", file_types=[".pdf"])
                    pdf_opsi = gr.Radio(
                        choices=[
                            "Sangat Kecil (Resolusi Layar/Web)", 
                            "Kecil (Kualitas Ebook)", 
                            "Sedang (Kualitas Printer)", 
                            "Bagus (Kualitas Prepress)"
                        ],
                        value="Sangat Kecil (Resolusi Layar/Web)",
                        label="Pilih Tingkat Kompresi"
                    )
                    pdf_btn = gr.Button("Kompres PDF Sekarang!", variant="primary")
                with gr.Column():
                    pdf_output = gr.File(label="📥 Hasil PDF (Siap Diunduh)")
                    pdf_status = gr.Textbox(label="Status", interactive=False, lines=2)
                    # MENGGUNAKAN GALLERY UNTUK SEMUA HALAMAN
                    pdf_preview = gr.Gallery(
                        label="👁️ Preview Dokumen (Maks. 50 Halaman)", 
                        columns=3, # Ditampilkan 3 ke samping agar rapi
                        height=500, # Tinggi kotak galeri
                        object_fit="contain"
                    )
            
            pdf_btn.click(
                fn=kompres_pdf, 
                inputs=[pdf_input, pdf_opsi], 
                outputs=[pdf_output, pdf_status, pdf_preview]
            )

        # TAB 2: WORD
        with gr.TabItem("📘 Kompres Word (.docx)"):
            with gr.Row():
                with gr.Column():
                    word_input = gr.File(label="Unggah File Word (.docx)", file_types=[".docx"])
                    word_opsi = gr.Radio(
                        choices=[
                            "Sangat Agresif (Ukuran Paling Kecil)", 
                            "Standar (Rekomendasi)", 
                            "Ringan (Kualitas Gambar Terjaga)"
                        ],
                        value="Standar (Rekomendasi)",
                        label="Pilih Tingkat Kompresi"
                    )
                    word_btn = gr.Button("Kompres Word Sekarang!", variant="primary")
                with gr.Column():
                    word_output = gr.File(label="📥 Hasil Word (Siap Diunduh)")
                    word_status = gr.Textbox(label="Status", interactive=False, lines=2)
                    word_preview = gr.Textbox(label="👁️ Preview Teks Word (5 Paragraf Pertama)", interactive=False, lines=6)
            
            word_btn.click(
                fn=kompres_word, 
                inputs=[word_input, word_opsi], 
                outputs=[word_output, word_status, word_preview]
            )

app.launch()