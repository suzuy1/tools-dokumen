import os
import pypandoc

def md_ke_word(input_file):
    if input_file is None: 
        return None, "❌ Silakan unggah file Markdown (.md) terlebih dahulu.", None
        
    if not input_file.name.lower().endswith(('.md', '.markdown')):
        return None, "❌ File harus berformat .md", None
        
    output_path = "Hasil_Konversi_MD.docx"
    
    try:
        # Konversi MD ke Word menggunakan Pandoc (mempertahankan semua format)
        pypandoc.convert_file(input_file.name, 'docx', outputfile=output_path)
        
        # Ekstrak teks langsung dari file Markdown untuk preview
        with open(input_file.name, 'r', encoding='utf-8') as f:
            isi_md = f.read()
            
        # Ambil 5 baris pertama yang ada isinya untuk preview
        baris_preview = [baris.strip() for baris in isi_md.split('\n') if baris.strip()][:5]
        preview_teks = "\n".join(baris_preview)
        
        if not preview_teks:
            preview_teks = "[File Markdown tidak memiliki teks]"
            
        # Kalkulasi ukuran (dalam KB karena file MD biasanya kecil)
        ukuran_awal = os.path.getsize(input_file.name) / 1024
        ukuran_akhir = os.path.getsize(output_path) / 1024
        
        return output_path, f"✅ Sukses! Markdown diubah ke Word.\nUkuran: {ukuran_awal:.2f} KB ➡️ {ukuran_akhir:.2f} KB", preview_teks
    except Exception as e:
        return None, f"❌ Terjadi kesalahan konversi: {str(e)}", None