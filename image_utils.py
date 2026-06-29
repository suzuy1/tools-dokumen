import os
from PIL import Image

def foto_ke_pdf(files, urutan_kustom):
    if not files: 
        return None, "❌ Silakan unggah foto terlebih dahulu.", []
        
    output_path = "Foto_ke_PDF_Selesai.pdf"
    file_paths = [f.name for f in files]
    
    # 1. Logika Mengatur Urutan Kustom sesuai Input User
    if urutan_kustom.strip():
        try:
            indeks_baru = [int(x.strip()) - 1 for x in urutan_kustom.split(",") if x.strip()]
            if any(i < 0 or i >= len(file_paths) for i in indeks_baru):
                return None, f"❌ Urutan salah! Pastikan angka antara 1 sampai {len(file_paths)}.", file_paths
            file_paths = [file_paths[i] for i in indeks_baru]
        except ValueError:
            return None, "❌ Format urutan salah! Gunakan angka dipisah koma. Contoh: 2, 1, 3", file_paths

    # ==========================================
    # LOGIKA REVISI: FULL FORMAT TANPA MARGIN
    # ==========================================
    pdf_pages = []
    try:
        for path in file_paths:
            img = Image.open(path)
            
            # Jika foto punya format transparan (RGBA seperti PNG), ubah ke RGB biasa
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            # Fotonya langsung dimasukkan ke dalam list tanpa media kertas tambahan
            # Ini akan membuat halaman PDF berukuran 100% pas dengan ukuran foto (Tanpa Margin)
            pdf_pages.append(img)
            
        if pdf_pages:
            # Simpan semua halaman foto menjadi satu file PDF utuh
            pdf_pages[0].save(output_path, save_all=True, append_images=pdf_pages[1:])
            return output_path, f"✅ Berhasil mengubah {len(pdf_pages)} foto menjadi PDF Full Format tanpa margin!", file_paths
        else:
            return None, "❌ Tidak ada foto valid yang bisa diproses.", []
            
    except Exception as e:
        return None, f"❌ Terjadi kesalahan: {str(e)}", []