# Panduan Training di Google Colab (100% Aman & Efisien)

Dokumen ini menjelaskan tata cara melatih model **Edge-VLM Diagnostic** di Google Colab menggunakan alokasi **Compute Units (A100 / T4)** secara legal, aman dari filter otomatis Google, dan dengan integrasi penyimpanan checkpoint otomatis ke Google Drive.

---

## 1. Persiapan Lingkungan Colab

### A. Memilih Jenis Runtime (GPU)
1. Buka file notebook di Google Colab (unggah file `.ipynb` dari folder `notebooks/`).
2. Masuk ke menu **Runtime** -> **Change runtime type**.
3. Pilih Hardware Accelerator:
   - **A100 GPU:** Direkomendasikan untuk training cepat (~1-2 jam selesai).
   - **T4 GPU:** Pilihan hemat Compute Units (~4-6 jam selesai dengan batch size lebih kecil).
4. Pastikan opsi runtime Python 3 dipilih.

### B. Menghubungkan Google Drive (Auto-Checkpoint)
Training deep learning wajib menyimpan model ke Google Drive agar jika sesi runtime Colab terputus, bobot model yang sudah dilatih tidak hilang.

```python
from google.colab import drive
drive.mount('/content/drive')
```
Folder output otomatis diarahkan ke: `/content/drive/MyDrive/Edge-VLM-Model/`.

---

## 2. Tahapan Eksekusi Notebook

Proyek ini dibagi menjadi 4 notebook modular di folder `notebooks/`:

1. **`01_Dataset_Synthesis_and_Prep.ipynb`**
   - Menyiapkan pasangan gambar dan teks tanya-jawab diagnosis perangkat keras (otomotif motor injeksi, sirkuit PCB/ESP32, dan drone).
   - Mengonversi format dataset ke standar Hugging Face `datasets` & ShareGPT Vision JSON format.
   - Perkiraan waktu: 10 - 15 menit.

2. **`02_VLM_QLoRA_Training_A100.ipynb`**
   - Memuat base model `Qwen/Qwen2-VL-2B-Instruct` dengan kuantisasi 4-bit (BitsAndBytes).
   - Menerapkan adapter LoRA (Low-Rank Adaptation) pada vision-projection dan attention layers.
   - Menjalankan `SFTTrainer` dari library Hugging Face TRL / Unsloth.
   - Dilengkapi callback logging real-time (Loss Curve, Learning Rate schedule, evaluasi validasi).
   - Perkiraan konsumsi: ~15 - 25 Compute Units pada GPU A100.

3. **`03_Quantization_GGUF_Edge_Export.ipynb`**
   - Menggabungkan (*merge*) LoRA adapter ke base model menjadi satu kesatuan bobot mandiri.
   - Melakukan kuantisasi ke format **GGUF (Q4_K_M dan Q8_0)** agar bisa dijalankan di CPU laptop dan Raspberry Pi via Ollama atau llama.cpp.
   - Mengekspor model ke ONNX / TFLite untuk penggunaan di Android.
   - Perkiraan konsumsi: ~5 - 10 Compute Units.

4. **`04_Live_Gradio_Demo_and_HF_Spaces.ipynb`**
   - Membangun antarmuka web interaktif berbasis Gradio di Colab.
   - Pengguna bisa upload foto mesin/PCB, model langsung merespons dengan deteksi komponen dan analisis kerusakan.
   - Siap di-deploy langsung ke Hugging Face Spaces secara gratis!

---

## 3. Aturan Keamanan Penting Colab

- **JANGAN** menjalankan script tunnel remote SSH (seperti `tmate`, `ngrok`, dsb.) karena melanggar *Terms of Service* Google Colab.
- Semua eksekusi berjalan 100% murni di cell Jupyter Notebook standar.
- Setiap error eksekusi akan tertangkap oleh blok `try...except` dan menampilkan pesan log yang rapi untuk langsung didebug.
