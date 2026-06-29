import gradio as gr
import subprocess
import os
import zipfile
import tempfile
import shutil
import io
from PIL import Image
import fitz  # PyMuPDF
import docx
from pypdf import PdfMerger, PdfReader, PdfWriter

# ==========================================
# FUNGSI CORE ILovePDF
# ==========================================

# 1. KOMPRES PDF
def kompres_pdf(input_file, tingkat_kompresi):
    if input_file is None: return None, "Unggah file PDF terlebih dahulu.", []
    input_path = input_file.name
    output_path = "hasil_kompresi.pdf"
    kualitas_map = {
        "Sangat Kecil (Resolusi Layar/Web)": '/screen',
        "Kecil (Kualitas Ebook)": '/ebook',
        "Sedang (Kualitas Printer)": '/printer',
        "Bagus (Kualitas Prepress)": '/prepress'
    }
    perintah_gs = ["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", f"-dPDFSETTINGS={kualitas_map[tingkat_kompresi]}", "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-sOutputFile={output_path}", input_path]
    try:
        subprocess.run(perintah_gs, check=True)
        preview_images = []
        try:
            doc = fitz.open(output_path)
            for i in range(min(len(doc), 30)):
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                preview_images.append(img)
        except Exception: pass
        ukuran_awal = os.path.getsize(input_path) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        return output_path, f"✅ Sukses!\nUkuran: {ukuran_awal:.2f} MB ➡️ {ukuran_akhir:.2f} MB", preview_images
    except Exception as e: return None, f"❌ Error: {str(e)}", []

# 2. GABUNG PDF (MERGE)
def gabung_pdf(files):
    if not files: return None, "Silakan pilih minimal 2 file PDF."
    if len(files) < 2: return None, "Pilih minimal 2 file untuk digabungkan!"
    
    output_path = "PDF_Gabungan_Selesai.pdf"
    merger = PdfMerger()
    
    try:
        for file in files:
            merger.append(file.name)
        merger.write(output_path)
        merger.close()
        
        info = f"✅ Berhasil menggabungkan {len(files)} file PDF!"
        return output_path, info
    except Exception as e:
        return None, f"❌ Gagal menggabungkan: {str(e)}"

# 3. PISAH PDF (SPLIT BY RANGE)
def pisah_pdf(input_file, rentang_halaman):
    if input_file is None: return None, "Unggah file PDF terlebih dahulu."
    if not rentang_halaman: return None, "Masukkan rentang halaman (contoh: 1-3)."
    
    output_path = "PDF_Potongan_Selesai.pdf"
    try:
        reader = PdfReader(input_file.name)
        writer = PdfWriter()
        
        # Parsing input rentang (misal: "1-3" menjadi start=0, end=3)
        parts = rentang_halaman.split('-')
        start_page = int(parts[0].strip()) - 1
        end_page = int(parts[1].strip())
        
        if start_page < 0 or end_page > len(reader.pages) or start_page >= end_page:
            return None, f"❌ Rentang tidak valid. File ini memiliki {len(reader.pages)} halaman."
            
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])
            
        with open(output_path, "wb") as f:
            writer.write(f)
            
        return output_path, f"✅ Berhasil memotong halaman {rentang_halaman} ({end_page - start_page} halaman)."
    except Exception as e:
        return None, f"❌ Error saat memisahkan: Digigit format tidak sesuai (Gunakan format: Angka-Angka)"

# 4. KOMPRES WORD
def kompres_word(input_file, tingkat_kompresi):
    if input_file is None: return None, "Unggah file Word (.docx) terlebih dahulu.", None
    if not input_file.name.lower().endswith('.docx'): return None, "Gunakan file .docx", None
    output_path = "hasil_kompresi.docx"
    kualitas_map = {"Sangat Agresif (Ukuran Paling Kecil)": (40, 800), "Standar (Rekomendasi)": (60, 1200), "Ringan (Kualitas Gambar Terjaga)": (80, 1600)}
    kualitas_jpeg, max_lebar = kualitas_map[tingkat_kompresi]
    temp_dir = tempfile.mkdtemp()
    gambar_diproses = 0
    try:
        with zipfile.ZipFile(input_file.name, 'r') as zip_ref: zip_ref.extractall(temp_dir)
        media_path = os.path.join(temp_dir, 'word', 'media')
        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                file_path = os.path.join(media_path, filename)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = Image.open(file_path)
                        if img.width > max_lebar:
                            img = img.resize((max_lebar, int(img.height * (max_lebar / img.width))), Image.Resampling.LANCZOS)
                        if filename.lower().endswith(('.jpg', '.jpeg')): img.save(file_path, "JPEG", optimize=True, quality=kualitas_jpeg)
                        elif filename.lower().endswith('.png'): img.save(file_path, "PNG", optimize=True)
                        gambar_diproses += 1
                    except Exception: pass
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx_zip:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    docx_zip.write(full_path, os.path.relpath(full_path, temp_dir))
        try:
            doc_obj = docx.Document(output_path)
            preview_teks = "\n\n".join([p.text.strip() for p in doc_obj.paragraphs if p.text.strip()][:5])
        except Exception: preview_teks = "[Gagal memuat preview]"
        ukuran_awal = os.path.getsize(input_file.name) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        return output_path, f"✅ Sukses! {gambar_diproses} gambar dikompres.\nUkuran: {ukuran_awal:.2f} MB ➡️ {ukuran_akhir:.2f} MB", preview_teks
    except Exception as e: return None, f"❌ Error: {str(e)}", None
    finally: shutil.rmtree(temp_dir)

# ==========================================
# INTERFACE DESIGN (ILovePDF Clone Look)
# ==========================================
with gr.Blocks(title="Klon ILovePDF Saya", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🛠️ Welcome to My-ILovePDF (100% Gratis & Selamanya)")
    gr.Markdown("Solusi lengkap untuk mengolah dokumen PDF dan Word secara instan langsung di server tanpa biaya.")
    
    with gr.Tabs():
        # TAB 1: GABUNG PDF
        with gr.TabItem("🔗 Gabung PDF"):
            gr.Markdown("### Gabungkan beberapa file PDF menjadi satu dokumen urutan sesuai keinginan.")
            with gr.Row():
                with gr.Column():
                    merge_input = gr.File(label="Pilih Banyak File PDF Sekaligus", file_count="multiple", file_types=[".pdf"])
                    merge_btn = gr.Button("Gabungkan PDF!", variant="primary")
                with gr.Column():
                    merge_output = gr.File(label="📥 Unduh PDF Gabungan")
                    merge_status = gr.Textbox(label="Status", interactive=False)
            merge_btn.click(fn=gabung_pdf, inputs=[merge_input], outputs=[merge_output, merge_status])

        # TAB 2: PISAH PDF
        with gr.TabItem("✂️ Pisah PDF"):
            gr.Markdown("### Ambil rentang halaman tertentu dari satu file PDF.")
            with gr.Row():
                with gr.Column():
                    split_input = gr.File(label="Unggah PDF yang Mau Dipotong", file_types=[".pdf"])
                    split_range = gr.Textbox(label="Rentang Halaman (Contoh: 1-5 atau 3-10)", placeholder="Format: AngkaAwal-AngkaAkhir")
                    split_btn = gr.Button("Potong PDF Sekarang!", variant="primary")
                with gr.Column():
                    split_output = gr.File(label="📥 Unduh Potongan PDF")
                    split_status = gr.Textbox(label="Status", interactive=False)
            split_btn.click(fn=pisah_pdf, inputs=[split_input, split_range], outputs=[split_output, split_status])

        # TAB 3: KOMPRES PDF
        with gr.TabItem("📕 Kompres PDF"):
            with gr.Row():
                with gr.Column():
                    pdf_input = gr.File(label="Unggah File PDF", file_types=[".pdf"])
                    pdf_opsi = gr.Radio(choices=["Sangat Kecil (Resolusi Layar/Web)", "Kecil (Kualitas Ebook)", "Sedang (Kualitas Printer)", "Bagus (Kualitas Prepress)"], value="Sangat Kecil (Resolusi Layar/Web)", label="Tingkat Kompresi")
                    pdf_btn = gr.Button("Kompres PDF!", variant="primary")
                with gr.Column():
                    pdf_output = gr.File(label="📥 Hasil PDF")
                    pdf_status = gr.Textbox(label="Status", interactive=False)
                    pdf_preview = gr.Gallery(label="👁️ Preview Hasil", columns=4, height=400, object_fit="contain")
            pdf_btn.click(fn=kompres_pdf, inputs=[pdf_input, pdf_opsi], outputs=[pdf_output, pdf_status, pdf_preview])

        # TAB 4: KOMPRES WORD
        with gr.TabItem("📘 Kompres Word"):
            with gr.Row():
                with gr.Column():
                    word_input = gr.File(label="Unggah File Word (.docx)", file_types=[".docx"])
                    word_opsi = gr.Radio(choices=["Sangat Agresif (Ukuran Paling Kecil)", "Standar (Rekomendasi)", "Ringan (Kualitas Gambar Terjaga)"], value="Standar (Rekomendasi)", label="Tingkat Kompresi")
                    word_btn = gr.Button("Kompres Word!", variant="primary")
                with gr.Column():
                    word_output = gr.File(label="📥 Hasil Word")
                    word_status = gr.Textbox(label="Status", interactive=False)
                    word_preview = gr.Textbox(label="👁️ Preview Teks", interactive=False, lines=5)
            word_btn.click(fn=kompres_word, inputs=[word_input, word_opsi], outputs=[word_output, word_status, word_preview])

app.launch()