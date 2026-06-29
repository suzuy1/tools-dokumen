import gradio as gr

# Import semua fungsi dari file modul kita
from pdf_utils import kompres_pdf, gabung_pdf, pisah_pdf, pdf_ke_word
from word_utils import kompres_word
from image_utils import foto_ke_pdf

# Fungsi perantara untuk menampilkan pratinjau foto instan saat di-upload
def update_galeri_foto(files):
    if not files: return []
    return [f.name for f in files]

# ==========================================
# ANTARMUKA PENGGUNA (UI) GRADIO
# ==========================================
with gr.Blocks(title="Klon ILovePDF Saya", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🛠️ Welcome to My-ILovePDF (100% Gratis & Selamanya)")
    gr.Markdown("Solusi lengkap pengolah dokumen PDF, Word, dan Foto secara instan tanpa biaya.")
    
    with gr.Tabs():
        # TAB 1: GABUNG PDF
        with gr.TabItem("🔗 Gabung PDF"):
            with gr.Row():
                with gr.Column():
                    merge_input = gr.File(label="Pilih Banyak File PDF Sekaligus", file_count="multiple", file_types=[".pdf"])
                    merge_btn = gr.Button("Gabungkan PDF!", variant="primary")
                with gr.Column():
                    merge_output = gr.File(label="📥 Unduh PDF Gabungan")
                    merge_status = gr.Textbox(label="Status", interactive=False)
                    merge_preview = gr.Gallery(label="👁️ Preview Hasil Gabungan", columns=4, height=300, object_fit="contain")
            merge_btn.click(fn=gabung_pdf, inputs=[merge_input], outputs=[merge_output, merge_status, merge_preview])

        # TAB 2: PISAH PDF
        with gr.TabItem("✂️ Pisah PDF"):
            with gr.Row():
                with gr.Column():
                    split_input = gr.File(label="Unggah PDF yang Mau Dipotong", file_types=[".pdf"])
                    split_range = gr.Textbox(label="Rentang Halaman (Contoh: 1-5)", placeholder="Format: AngkaAwal-AngkaAkhir")
                    split_btn = gr.Button("Potong PDF Sekarang!", variant="primary")
                with gr.Column():
                    split_output = gr.File(label="📥 Unduh Potongan PDF")
                    split_status = gr.Textbox(label="Status", interactive=False)
                    split_preview = gr.Gallery(label="👁️ Preview Hasil Potongan", columns=4, height=300, object_fit="contain")
            split_btn.click(fn=pisah_pdf, inputs=[split_input, split_range], outputs=[split_output, split_status, split_preview])

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
                    pdf_preview = gr.Gallery(label="👁️ Preview Hasil Kompresi", columns=4, height=300, object_fit="contain")
            pdf_btn.click(fn=kompres_pdf, inputs=[pdf_input, pdf_opsi], outputs=[pdf_output, pdf_status, pdf_preview])

        # TAB 4: PDF TO WORD (REVISI DENGAN INPUT PREVIEW)
        with gr.TabItem("🔄 PDF ke Word"):
            gr.Markdown("### Ubah dokumen PDF menjadi file Word (.docx) yang bisa diedit kembali.")
            with gr.Row():
                with gr.Column():
                    pdf_to_word_input = gr.File(label="Unggah File PDF", file_types=[".pdf"])
                    pdf_to_word_btn = gr.Button("Konversi ke Word Now!", variant="primary")
                with gr.Column():
                    pdf_to_word_output = gr.File(label="📥 Unduh File Word (.docx)")
                    pdf_to_word_status = gr.Textbox(label="Status", interactive=False)
                    # MENGGUNAKAN TEXTBOX UNTUK PREVIEW HASIL EKSTRAKSI TEKS WORD
                    pdf_to_word_preview = gr.Textbox(label="👁️ Preview Teks Hasil Konversi (5 Paragraf Pertama)", interactive=False, lines=5)
            pdf_to_word_btn.click(fn=pdf_ke_word, inputs=[pdf_to_word_input], outputs=[pdf_to_word_output, pdf_to_word_status, pdf_to_word_preview])

        # TAB 5: FOTO TO PDF + CUSTOM ORDER
        with gr.TabItem("🖼️ Foto ke PDF"):
            gr.Markdown("### Ubah kumpulan foto menjadi satu file PDF. Anda bisa mengatur urutan halaman lewat kolom di bawah.")
            with gr.Row():
                with gr.Column():
                    img_input = gr.File(label="Pilih atau Tarik Foto (Bisa Banyak Sekaligus)", file_count="multiple", file_types=[".jpg", ".jpeg", ".png"])
                    img_order = gr.Textbox(
                        label="✍️ Atur Urutan Halaman (Opsional)", 
                        placeholder="Contoh: 2, 1",
                        info="Biarkan kosong jika urutan foto di galeri pratinjau sudah benar."
                    )
                    img_btn = gr.Button("Konversi Foto ke PDF!", variant="primary")
                with gr.Column():
                    img_output = gr.File(label="📥 Unduh PDF Hasil Foto")
                    img_status = gr.Textbox(label="Status", interactive=False)
                    img_preview = gr.Gallery(label="👁️ Galeri Urutan Foto (Cek nomor urutannya di sini)", columns=3, height=300, object_fit="contain")
            
            img_input.change(fn=update_galeri_foto, inputs=[img_input], outputs=[img_preview])
            img_btn.click(fn=foto_ke_pdf, inputs=[img_input, img_order], outputs=[img_output, img_status, img_preview])

        # TAB 6: KOMPRES WORD
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