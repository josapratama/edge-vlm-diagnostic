# Panduan Publikasi Portfolio & Hugging Face Showcase

Dokumen ini menjelaskan strategi memaksimalkan nilai jual proyek **Edge-VLM Diagnostic** sebagai portofolio AI Engineering tingkat profesional.

---

## 1. Tiga Pilar Portofolio Terverifikasi (The Verification Triad)

Sebuah proyek AI diakui bernilai tinggi di mata industri jika memiliki 3 pilar yang saling terhubung:

1. **Hugging Face Hub (Model Repository & Card):**
   - Publikasikan model di profil Hugging Face: `https://huggingface.co/username/edge-vlm-hardware-diagnostic`
   - Sertakan **Model Card** komprehensif: arsitektur base model, ukuran dataset, hyperparameters training, evaluasi loss, dan contoh inferensi.
   - Sediakan bobot versi full precision (FP16), LoRA Adapter, dan file GGUF siap pakai.

2. **Hugging Face Space (Live Interactive Demo):**
   - Buat Space publik gratis berbasis **Gradio**.
   - Siapa pun (klien, recruiter, komunitas AI) dapat mengklik link demo, mengunggah foto mesin motor atau board PCB mereka sendiri, dan melihat model Anda menganalisis gambar tersebut secara langsung di browser tanpa perlu install apa pun.

3. **GitHub Repository (Clean Code & Open Engineering):**
   - Repositori GitHub terstruktur dengan lencana (*badges*), diagram arsitektur, script training reproducible, dan panduan deployment lengkap.

---

## 2. Struktur Narasi Portofolio (Untuk CV / LinkedIn)

Berikut adalah contoh deskripsi pencapaian teknis (*bullet points*) yang sangat kuat untuk dimasukkan ke CV atau portofolio LinkedIn Anda:

> **Edge-VLM: Multimodal Vision-Language Model for Edge Hardware & Automotive Diagnostics**
> * Developed an end-to-end Multimodal Vision-Language Model (VLM) based on Qwen2-VL (2B) for visual fault detection across motorcycle engines, PCB circuitry, and UAV/drone hardware.
> * Engineered a custom dataset of 3,000+ domain-specific visual QA pairs utilizing Chain-of-Thought (CoT) diagnostic reasoning.
> * Fine-tuned using 4-bit QLoRA on Google Colab A100 GPU, achieving low training loss while reducing GPU memory footprint by 65%.
> * Quantized model weights into GGUF 4-bit (Q4_K_M), enabling real-time local inference (>15 tokens/sec) on edge devices (Raspberry Pi 5 & mobile).
> * Published open-source model weights, interactive Gradio web demo on Hugging Face Spaces, and reproducible training pipeline on GitHub.

---

## 3. Checklist Sebelum Publikasi

- [ ] Upload bobot LoRA adapter ke Hugging Face Models.
- [ ] Upload file GGUF quant ke Hugging Face Models (kategori `gguf`).
- [ ] Buat `README.md` pada repositori Hugging Face lengkap dengan tag `vision`, `multimodal`, `qwen2-vl`, `edge-ai`.
- [ ] Deploy file `src/web/app.py` ke Hugging Face Spaces.
- [ ] Ambil screenshot atau rekam GIF demo interaktif untuk disematkan di GitHub `README.md`.
