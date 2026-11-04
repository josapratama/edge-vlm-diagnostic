# Arsitektur & Konsep Edge-VLM Diagnostic

## 1. Latar Belakang & Urgensi
Di era AI modern (2025/2026), model bahasa murni (Text-Only LLM) sudah menjadi komoditas umum. Tantangan revolusioner berikutnya adalah **Multimodal Vision-Language Models (VLM)** yang dapat **melihat, menganalisis, dan memberikan penalaran visual (Visual Reasoning)** terhadap objek fisik di dunia nyata.

Dalam industri otomotif, IoT, dan perakitan robotik/drone:
- Teknisi sering kesulitan mengidentifikasi kerusakan fisik (solder dingin, kapasitor terbakar, kabel sensor TPS terkelupas, jalur PCB putus, kebocoran fluida).
- Model Vision tradisional (seperti klasifikasi ResNet standar) hanya bisa memberikan label satu kata tanpa penjelasan logis.
- **Edge-VLM Diagnostic** memadukan kemampuan Computer Vision tingkat tinggi dengan Large Language Model berukuran kompak (**Qwen2-VL-2B-Instruct** atau **SmolVLM-2B**) yang di-fine-tune khusus untuk mendiagnosis kerusakan perangkat keras dan otomotif secara mendalam.

---

## 2. Diagram Alur Sistem (End-to-End Pipeline)

```
[ Input: Foto Mesin / PCB / Drone ]
                 │
                 ▼
    ┌──────────────────────────┐
    │  Vision Encoder (ViT)    │  --> Ekstraksi patch gambar beresolusi dinamis (Dynamic 2D-RoPE)
    └────────────┬─────────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │ Vision-to-Language Proj. │  --> Menyelaraskan embedding visual ke ruang token bahasa
    └────────────┬─────────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │ Small Language Model     │  --> Qwen2-VL / SmolVLM (2B Parameters)
    │ (Fine-Tuned with QLoRA)  │  --> Menerapkan Chain-of-Thought (CoT) Visual Reasoning
    └────────────┬─────────────┘
                 │
                 ▼
   [ Output Diagnostik Multimodal ]
   1. Deteksi Komponen Fisik (Bounding Box / Posisi)
   2. Temuan Kerusakan / Anomali Visual
   3. Penjelasan Penyebab & Rekomendasi Solusi Teknis
                 │
                 ▼
   [ Edge Optimization & Quantization ]
   - Konversi ke GGUF (Q4_K_M) untuk Ollama / llama.cpp di PC & Raspberry Pi 5
   - Konversi ke ONNX / TFLite untuk Android & Embedded Device
```

---

## 3. Komponen Utama Model

1. **Base Model:** `Qwen/Qwen2-VL-2B-Instruct`
   - Mendukung resolusi gambar dinamis tanpa cropping paksa.
   - Ukuran 2 miliar parameter (sangat pas untuk di-deploy di edge hardware dengan memori terbatas).
2. **Teknik Fine-Tuning:**
   - **QLoRA (4-bit NormalFloat Quantization):** Mengurangi konsumsi VRAM training dari 32GB menjadi hanya ~8-12GB VRAM, sangat hemat di GPU A100/T4 Colab.
   - **Rank $r=16$, Alpha $\alpha=32$** pada target modules `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`.
3. **Struktur Data Percakapan (ShareGPT Multimodal Format):**
   - Mendukung kombinasi token `<|image_pad|>` dengan teks instruksi teknis dalam Bahasa Indonesia & Bahasa Inggris.
