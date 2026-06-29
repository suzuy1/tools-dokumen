# 🗜️ Tools Dokumen Super (My-ILovePDF Clone)

Sebuah aplikasi web sumber terbuka (*open-source*) 100% gratis untuk memproses, memanipulasi, dan mengonversi berbagai format dokumen secara instan. Proyek ini dibangun sebagai alternatif mandiri dari layanan berbayar seperti ILovePDF, dengan mengutamakan privasi dan arsitektur modular.

Aplikasi ini berjalan dengan antarmuka pengguna (UI) interaktif yang ditenagai oleh **Gradio** dan pemrosesan tingkat tinggi di sisi server menggunakan Python.

---

## 🌟 Pengenalan Proyek
Mengelola dokumen seperti PDF, Word, dan gambar sering kali membutuhkan alat pihak ketiga yang membatasi ukuran file, membatasi jumlah proses per hari, atau mengharuskan biaya langganan premium. 

**Tools Dokumen Super** diciptakan untuk memecahkan masalah tersebut. Dengan mende-deploy aplikasi ini di server Anda sendiri (atau layanan gratis seperti Hugging Face Spaces), Anda memiliki kendali penuh atas dokumen Anda tanpa batasan apa pun. File Anda tidak disimpan di server pihak ketiga mana pun setelah proses selesai, menjadikannya sangat aman.

---

## 🚀 Fitur Utama

Aplikasi ini memiliki 7 alat utama yang dipisahkan ke dalam tab-tab yang mudah dinavigasi, lengkap dengan fitur **Galeri Pratinjau (Preview)** sebelum Anda mengunduh hasilnya:

1. **🔗 Gabung PDF (Merge)**
   Gabungkan banyak file PDF menjadi satu dokumen tunggal sesuai urutan yang Anda inginkan.
2. **✂️ Pisah PDF (Split)**
   Ekstrak halaman tertentu dari PDF menggunakan format rentang (contoh: 1-5).
3. **📕 Kompres PDF**
   Kecilkan ukuran file PDF (sangat efektif untuk PDF hasil scan) dengan pilihan tingkat kompresi tanpa merusak dokumen aslinya menggunakan mesin *Ghostscript*.
4. **🔄 PDF ke Word**
   Konversi dokumen PDF menjadi file Microsoft Word (`.docx`) yang dapat diedit ulang dengan tata letak (*layout*) dan tabel yang tetap dipertahankan.
5. **🖼️ Foto ke PDF**
   Ubah kumpulan gambar (JPG, JPEG, PNG) menjadi satu file PDF formal dengan tata letak kertas A4 Portrait standar. Dilengkapi fitur *Custom Order* untuk menyusun ulang urutan halaman.
6. **📘 Kompres Word**
   Otomatis mengecilkan ukuran file `.docx` yang membengkak dengan mengoptimalkan resolusi gambar-gambar di dalamnya tanpa merusak susunan teks.
7. **📝 MD ke Word**
   Konversi file dokumentasi Markdown (`.md`) menjadi file Word (`.docx`) utuh, mempertahankan struktur *heading*, tabel, dan kode di dalamnya.

---

## 🛠️ Teknologi yang Digunakan

Proyek ini menggunakan arsitektur modular Python dengan pustaka (*libraries*) terbaik di bidangnya:
* **Antarmuka (UI):** [Gradio](https://gradio.app/)
* **Pemrosesan PDF:** `pypdf`, `PyMuPDF` (fitz), dan `Ghostscript`
* **Konversi Dokumen:** `pdf2docx` dan `pypandoc` (Pandoc)
* **Pemrosesan Gambar:** `Pillow` (PIL)
* **Pemrosesan Word:** `python-docx`

---

## 📂 Struktur DirektORI

Kode aplikasi sengaja dipecah (*separation of concerns*) agar mudah dikembangkan di masa depan:

```text
tools-dokumen/
│
├── app.py               # File utama penyusun antarmuka (UI) dan routing Tab
├── pdf_utils.py         # Modul khusus logika manipulasi & konversi PDF
├── word_utils.py        # Modul khusus manipulasi MS Word (.docx)
├── image_utils.py       # Modul khusus pemrosesan foto ke PDF (Layout A4)
├── md_utils.py          # Modul khusus pengolahan Markdown (.md)
├── requirements.txt     # Daftar pustaka Python yang dibutuhkan
├── packages.txt         # Ketergantungan sistem operasi (Debian/Linux)
└── README.md            # Dokumentasi proyek

```

---

## 💻 Cara Instalasi & Menjalankan di Lokal (Localhost)

Jika Anda ingin menjalankan atau memodifikasi proyek ini di komputer lokal Anda, ikuti langkah-langkah berikut:

### 1. Kloning Repositori

```bash
git clone https://github.com/suzuy1/tools-dokumen.git
cd tools-dokumen

```

### 2. Instalasi Ketergantungan Sistem (Penting)

Aplikasi ini membutuhkan *Ghostscript* (untuk kompresi PDF) dan *Pandoc* (untuk Markdown).

* **Pengguna Linux/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install ghostscript pandoc

```


* **Pengguna macOS:**
```bash
brew install ghostscript pandoc

```


* **Pengguna Windows:** Silakan unduh dan instal *installer* resmi [Ghostscript](https://ghostscript.com/releases/gsdnld.html) dan [Pandoc](https://pandoc.org/installing.html) lalu tambahkan ke PATH *environment variables* Anda.

### 3. Instalasi Pustaka Python

Sangat disarankan menggunakan *Virtual Environment* (venv).

```bash
pip install -r requirements.txt

```

### 4. Jalankan Aplikasi

```bash
python app.py

```

Aplikasi akan berjalan dan dapat diakses melalui browser di alamat: `http://127.0.0.1:7860`

---

## 🤝 Kontribusi

Kontribusi, masalah (*issues*), dan permintaan fitur (*pull requests*) sangat diterima! Jika Anda memiliki ide untuk menambahkan alat baru (misalnya Proteksi PDF, Word ke PDF, dll), silakan *fork* repositori ini dan kirimkan kode Anda.

## 📝 Lisensi

Didistribusikan di bawah lisensi MIT. Anda bebas menggunakan, memodifikasi, dan mendistribusikan perangkat lunak ini secara gratis.

---

**Dikembangkan dengan bangga oleh:** M. Oriza Saltifa
