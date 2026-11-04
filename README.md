# Edge-VLM: Multimodal Vision-Language Model for Hardware & Automotive Diagnostics 🔬⚡

[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-yellow)](https://huggingface.co/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Edge AI](https://img.shields.io/badge/Edge%20AI-Raspberry%20Pi%205%20%7C%20Android%20%7C%20Ollama-blue)](https://github.com/josapratama/edge-vlm-diagnostic)

**Edge-VLM** adalah model kecerdasan buatan Multimodal Vision-Language Model (VLM) berbobot ringan (~2B parameter) yang dilatih khusus untuk melakukan **inspeksi visual dan diagnosis kerusakan perangkat keras fisik (hardware)**:
* 🏍️ **Sistem Injeksi Otomotif & Sepeda Motor:** Throttle Body, sensor TPS, injektor, spull stator, koil, dan kabel bodi.
* 🔌 **Sirkuit Elektronik & IoT:** Modul ESP32, Raspberry Pi, solderan dingin (*cold solder joints*), komponen SMD terbakar, dan jalur PCB putus.
* 🛸 **Hardware Drone & UAV:** ESC 4-in-1, motor brushless, flight controller, dan propeller aerodinamis.

Proyek ini dibangun dari dataset sintetis berbasis penalaran berantai (**Chain-of-Thought Visual Reasoning**), di-fine-tune menggunakan **4-bit QLoRA pada GPU A100**, dan dikuantisasi ke format **GGUF (Q4_K_M)** untuk inferensi lokal 100% offline di **Raspberry Pi 5** dan **smartphone Android**.

---

## 🌟 Fitur Utama

- 👁️ **Multimodal Dynamic Resolution:** Menggunakan arsitektur `Qwen2-VL-2B-Instruct` dengan patch visual dinamis, membaca detail kabel kecil atau noda gosong mikro tanpa cropping paksa.
- 🧠 **Structured Diagnostic Reasoning:** Menghasilkan output terstruktur (Identifikasi Komponen $\rightarrow$ Temuan Kerusakan $\rightarrow$ Akar Masalah $\rightarrow$ Rekomendasi Solusi Teknis).
- ⚡ **Ultra-Efficient Edge Quantization:** Model hasil kuantisasi hanya berukuran **~1.4 GB**, berjalan lancar di Raspberry Pi 5 (12-18 token/detik) dan laptop biasa tanpa GPU diskrit.
- ☁️ **Colab Pro Ready (100% Aman):** Dilengkapi 4 notebook mandiri yang aman dari batasan filter Colab, dengan penyimpanan checkpoint otomatis ke Google Drive.
- 🌐 **Interactive Gradio Web UI:** Siap dideploy ke **Hugging Face Spaces** untuk uji coba publik interaktif.

---

## 🏗️ Struktur Repositori

```
edge-vlm-diagnostic/
├── notebooks/                              # Jupyter Notebooks siap pakai di Colab
│   ├── 01_Dataset_Synthesis_and_Prep.ipynb # Generator dataset ShareGPT Vision
│   ├── 02_VLM_QLoRA_Training_A100.ipynb    # Pipeline QLoRA training di A100 GPU
│   ├── 03_Quantization_GGUF_Edge_Export.ipynb # Merge adapter & kompilasi GGUF
│   └── 04_Live_Gradio_Demo_and_HF_Spaces.ipynb # Web demo interaktif di Colab/HF
├── src/                                    # Python source code modular
│   ├── dataset/
│   │   ├── prompt_templates.py             # Template prompt diagnostik CoT
│   │   └── synthetic_generator.py          # Generator data sintetis otomotif/IoT
│   ├── training/
│   │   ├── train_config.py                 # Dataclasses hyperparameter training
│   │   └── vlm_trainer.py                  # Trainer script PyTorch & HuggingFace
│   ├── inference/
│   │   └── detector.py                     # Inference engine lokal
│   └── web/
│       └── app.py                          # Aplikasi web Gradio (HF Space)
├── docs/                                   # Dokumentasi arsitektur komprehensif
│   ├── 01_ARSITEKTUR_DAN_KONSEP_VLM.md
│   ├── 02_PANDUAN_TRAINING_DI_GOOGLE_COLAB.md
│   ├── 03_PANDUAN_EXPORT_DAN_DEPLOY_RASPBERRY_PI.md
│   └── 04_PORTFOLIO_SHOWCASE_DAN_HUGGINGFACE.md
├── requirements.txt
├── .gitignore
├── LICENSE                                 # Lisensi MIT
└── README.md
```

---

## 🚀 Panduan Eksekusi di Google Colab

1. Buka [Google Colab](https://colab.research.google.com).
2. Unggah file notebook berurutan dari folder `notebooks/`:
   - **Langkah 1:** Jalankan `01_Dataset_Synthesis_and_Prep.ipynb` untuk membuat dataset.
   - **Langkah 2:** Pilih GPU **A100**, jalankan `02_VLM_QLoRA_Training_A100.ipynb` (selesai dalam ~1-2 jam, menghabiskan ~15-25 Compute Units).
   - **Langkah 3:** Jalankan `03_Quantization_GGUF_Edge_Export.ipynb` untuk mengunduh model `.gguf`.
   - **Langkah 4:** Jalankan `04_Live_Gradio_Demo_and_HF_Spaces.ipynb` untuk menguji web UI.

---

## 🍓 Menjalankan Model di Raspberry Pi 5 (Offline)

Setelah mengunduh file `edge-vlm-diag-q4_k_m.gguf` dari Google Drive:
```bash
# Jalankan via llama.cpp di Raspberry Pi 5
./llama-llava-cli \
    -m models/edge-vlm-diag-q4_k_m.gguf \
    --mmproj models/mmproj-model-f16.gguf \
    --image /path/to/foto_motor.jpg \
    -p "Periksa komponen ini dan deteksi kerusakannya."
```

---

## 📄 Lisensi

Proyek ini berlisensi [MIT](LICENSE). Bebas digunakan, dikembangkan, dan dipublikasikan untuk keperluan riset maupun komersial.
