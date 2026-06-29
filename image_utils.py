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
    # LOGIKA REVISI: LAYOUT KERTAS A4 (ALA WORD)
    # ==========================================
    # Ukuran standar kertas A4 Portrait dalam pixel (Resolusi tajam 150 DPI)
    A4_LEBAR = 1240
    A4_TINGGI = 1754
    MARGIN = 80 # Jarak kosong di pinggir kertas/border (seperti di Word)
    
    # Area maksimal yang boleh diisi oleh foto setelah dikurangi margin
    MAX_FOTO_LEBAR = A4_LEBAR - (MARGIN * 2)
    MAX_FOTO_TINGGI = A4_TINGGI - (MARGIN * 2)

    pdf_pages = []
    try:
        for path in file_paths:
            img = Image.open(path)
            
            # Jika foto punya format transparan (RGBA seperti PNG), ubah ke RGB biasa
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            # Langkah A: Buat "kertas putih" kosong ukuran A4 Portrait
            kertas_putih = Image.new("RGB", (A4_LEBAR, A4_TINGGI), "white")
            
            # Langkah B: Perkecil/sesuaikan foto agar pas di area cetak kertas (rasio foto tetap terjaga, tidak gepeng)
            img.thumbnail((MAX_FOTO_LEBAR, MAX_FOTO_TINGGI), Image.Resampling.LANCZOS)
            
            # Langkah C: Hitung posisi koordinat X dan Y agar foto berada tepat di tengah-tengah kertas putih
            x_pos = (A4_LEBAR - img.width) // 2
            y_pos = (A4_TINGGI - img.height) // 2
            
            # Langkah D: "Tempelkan" foto tersebut ke atas kertas putih
            kertas_putih.paste(img, (x_pos, y_pos))
            
            # Masukkan kertas yang sudah ada fotonya ke daftar halaman PDF
            pdf_pages.append(kertas_putih)
            
        if pdf_pages:
            # Simpan semua kertas putih tadi menjadi satu file PDF utuh
            pdf_pages[0].save(output_path, save_all=True, append_images=pdf_pages[1:])
            return output_path, f"✅ Berhasil mengubah {len(pdf_pages)} foto menjadi PDF dengan Layout A4 standar!", file_paths
        else:
            return None, "❌ Tidak ada foto valid yang bisa diproses.", []
            
    except Exception as e:
        return None, f"❌ Terjadi kesalahan: {str(e)}", []