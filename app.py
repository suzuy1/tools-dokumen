import gradio as gr

# Import fungsi dari file modul yang sudah kita pisah
from pdf_utils import kompres_pdf, gabung_pdf, pisah_pdf
from word_utils import kompres_word

# ==========================================
# ANTARMUKA PENGGUNA (UI) GRADIO
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
                    merge_preview = gr.Gallery(label="👁️ Preview Hasil Gabungan (Maks. 30 Halaman)", columns=4, height=400, object_fit="contain")
            merge_btn.click(fn=gabung_pdf, inputs=[merge_input], outputs=[merge_output, merge_status, merge_preview])

        # TAB 2: PISAH PDF
        with gr.TabItem("✂️ Pisah PDF"):
            gr.Markdown("### Ambil rentang halaman tertentu dari satu file PDF.")
            with gr.Row():
                with gr.Column():
                    split_input = gr.File(label="Unggah PDF yang Mau Dipotong", file_types=[".pdf"])
                    split_range = gr.Textbox(label="Rentang Halaman (Contoh: 1-5)", placeholder="Format: AngkaAwal-AngkaAkhir")
                    split_btn = gr.Button("Potong PDF Sekarang!", variant="primary")
                with gr.Column():
                    split_output = gr.File(label="📥 Unduh Potongan PDF")
                    split_status = gr.Textbox(label="Status", interactive=False)
                    split_preview = gr.Gallery(label="👁️ Preview Hasil Potongan (Maks. 30 Halaman)", columns=4, height=400, object_fit="contain")
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
                    pdf_preview = gr.Gallery(label="👁️ Preview Hasil Kompresi (Maks. 30 Halaman)", columns=4, height=400, object_fit="contain")
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
                    word_preview = gr.Textbox(label="👁️ Preview Teks (5 Paragraf Pertama)", interactive=False, lines=5)
            word_btn.click(fn=kompres_word, inputs=[word_input, word_opsi], outputs=[word_output, word_status, word_preview])

app.launch()