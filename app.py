import gradio as gr
import subprocess
import os
import zipfile
import tempfile
import shutil
from PIL import Image

# ==========================================
# FUNGSI 1: KOMPRES PDF
# ==========================================
def kompres_pdf(input_file, tingkat_kompresi):
    if input_file is None:
        return None, "Silakan unggah file PDF terlebih dahulu."
    
    if not input_file.name.lower().endswith('.pdf'):
        return None, "Maaf, ini tab khusus PDF. Gunakan tab Word untuk file .docx"

    input_path = input_file.name
    output_path = "hasil_kompresi.pdf"
    
    kualitas_map = {
        "Sangat Kecil (Resolusi Layar/Web)": '/screen',
        "Kecil (Kualitas Ebook)": '/ebook',
        "Sedang (Kualitas Printer)": '/printer',
        "Bagus (Kualitas Prepress)": '/prepress'
    }
    
    kualitas_gs = kualitas_map[tingkat_kompresi]
    
    perintah_gs = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={kualitas_gs}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    try:
        subprocess.run(perintah_gs, check=True)
        ukuran_awal = os.path.getsize(input_path) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        pesan = f"✅ Sukses!\nUkuran Awal: {ukuran_awal:.2f} MB ➡️ Ukuran Akhir: {ukuran_akhir:.2f} MB"
        return output_path, pesan
    except Exception as e:
        return None, f"❌ Terjadi kesalahan: {str(e)}"

# ==========================================
# FUNGSI 2: KOMPRES WORD (.DOCX)
# ==========================================
def kompres_word(input_file, tingkat_kompresi):
    if input_file is None:
        return None, "Silakan unggah file Word (.docx) terlebih dahulu."
    
    if not input_file.name.lower().endswith('.docx'):
        return None, "Maaf, ini tab khusus Word. Gunakan tab PDF untuk file .pdf"

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
                    
        ukuran_awal = os.path.getsize(input_path) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        
        pesan = (f"✅ Sukses! {gambar_diproses} gambar dikompres.\n"
                 f"Ukuran Awal: {ukuran_awal:.2f} MB ➡️ Ukuran Akhir: {ukuran_akhir:.2f} MB")
        return output_path, pesan
        
    except Exception as e:
        return None, f"❌ Terjadi kesalahan: {str(e)}"
    finally:
        shutil.rmtree(temp_dir)

# ==========================================
# ANTARMUKA PENGGUNA (UI) DENGAN TAB
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
                    pdf_output = gr.File(label="Hasil PDF (Siap Diunduh)")
                    pdf_status = gr.Textbox(label="Status", interactive=False, lines=2)
            
            pdf_btn.click(fn=kompres_pdf, inputs=[pdf_input, pdf_opsi], outputs=[pdf_output, pdf_status])

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
                    word_output = gr.File(label="Hasil Word (Siap Diunduh)")
                    word_status = gr.Textbox(label="Status", interactive=False, lines=2)
            
            word_btn.click(fn=kompres_word, inputs=[word_input, word_opsi], outputs=[word_output, word_status])

app.launch()