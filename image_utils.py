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
            # Mengubah input "2, 1" menjadi list angka [1, 0] (karena indeks python mulai dari 0)
            indeks_baru = [int(x.strip()) - 1 for x in urutan_kustom.split(",") if x.strip()]
            
            # Validasi apakah angka yang dimasukkan user masuk akal
            if any(i < 0 or i >= len(file_paths) for i in indeks_baru):
                return None, f"❌ Urutan salah! Pastikan angka antara 1 sampai {len(file_paths)}.", file_paths
                
            # Susun ulang posisi file berdasarkan urutan baru
            file_paths = [file_paths[i] for i in indeks_baru]
        except ValueError:
            return None, "❌ Format urutan salah! Gunakan angka dipisah koma. Contoh: 2, 1, 3", file_paths

    # 2. Proses Menggabungkan Foto Menjadi PDF
    images = []
    try:
        for path in file_paths:
            img = Image.open(path)
            # Karena PDF tidak mendukung format warna RGBA (transparan seperti di PNG), 
            # kita harus ubah ke RGB (Background Putih/Polos) agar tidak error
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            images.append(img)
            
        if images:
            # Simpan foto pertama, lalu tempel foto sisanya di halaman berikutnya
            images[0].save(output_path, save_all=True, append_images=images[1:])
            return output_path, f"✅ Berhasil mengubah {len(images)} foto menjadi PDF sesuai urutan!", file_paths
        else:
            return None, "❌ Tidak ada foto valid yang bisa diproses.", []
    except Exception as e:
        return None, f"❌ Terjadi kesalahan: {str(e)}", []