import os
import zipfile
import tempfile
import shutil
from PIL import Image
import docx

def kompres_word(input_file, tingkat_kompresi):
    if input_file is None: 
        return None, "Unggah file Word (.docx) terlebih dahulu.", None
    if not input_file.name.lower().endswith('.docx'): 
        return None, "Gunakan file .docx", None
        
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
        with zipfile.ZipFile(input_file.name, 'r') as zip_ref: 
            zip_ref.extractall(temp_dir)
            
        media_path = os.path.join(temp_dir, 'word', 'media')
        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                file_path = os.path.join(media_path, filename)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = Image.open(file_path)
                        if img.width > max_lebar:
                            img = img.resize((max_lebar, int(img.height * (max_lebar / img.width))), Image.Resampling.LANCZOS)
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
                    docx_zip.write(full_path, os.path.relpath(full_path, temp_dir))
                    
        try:
            doc_obj = docx.Document(output_path)
            preview_teks = "\n\n".join([p.text.strip() for p in doc_obj.paragraphs if p.text.strip()][:5])
        except Exception: 
            preview_teks = "[Gagal memuat preview]"
            
        ukuran_awal = os.path.getsize(input_file.name) / (1024 * 1024)
        ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
        return output_path, f"✅ Sukses! {gambar_diproses} gambar dikompres.\nUkuran: {ukuran_awal:.2f} MB ➡️ {ukuran_akhir:.2f} MB", preview_teks
    except Exception as e: 
        return None, f"❌ Error: {str(e)}", None
    finally: 
        shutil.rmtree(temp_dir)