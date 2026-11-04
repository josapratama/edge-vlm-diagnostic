# Panduan Deployment Edge (Raspberry Pi & Android)

Setelah model selesai dilatih dan dikuantisasi menjadi format **GGUF**, model ini dapat dijalankan **100% offline tanpa koneksi internet** di komputer lokal, laptop, smartphone Android, maupun **Raspberry Pi 5 (8GB)**.

---

## 1. Menjalankan di Raspberry Pi 5 via llama.cpp / Ollama

### Spesifikasi yang Disarankan:
- **Board:** Raspberry Pi 5 (RAM 8GB sangat disarankan) atau Raspberry Pi 4B (RAM 8GB).
- **Storage:** MicroSD / NVMe SSD dengan sisa ruang minimal 6GB.
- **OS:** Raspberry Pi OS 64-bit (Debian Bookworm).

### Langkah Instalasi di Raspberry Pi:

1. Unduh file model hasil kuantisasi (contoh: `edge-vlm-diag-q4_k_m.gguf` dan `mmproj-model-f16.gguf` untuk vision projector).
2. Pasang `llama.cpp` dengan kompilasi teroptimasi ARM NEON:
   ```bash
   sudo apt update && sudo apt install -y build-essential cmake git
   git clone https://github.com/ggerganov/llama.cpp
   cd llama.cpp
   cmake -B build
   cmake --build build --config Release -j4
   ```
3. Jalankan inferensi multimodal via terminal:
   ```bash
   ./build/bin/llama-llava-cli \
       -m models/edge-vlm-diag-q4_k_m.gguf \
       --mmproj models/mmproj-model-f16.gguf \
       --image /path/to/foto_motor.jpg \
       -p "Periksa foto motor ini. Apakah ada komponen yang tidak normal atau rusak?" \
       --temp 0.2
   ```

### Kecepatan Inferensi di Raspberry Pi 5:
- **Load Time:** ~2-3 detik.
- **Vision Encoding:** ~1.2 detik per gambar.
- **Token Generation:** ~12 - 18 token/detik (sangat responsif untuk asisten teknisi langsung di lapangan).

---

## 2. Menjalankan di Smartphone Android (via Termux & Ollama Mobile)

1. Pasang aplikasi **Termux** di HP Android Anda.
2. Pasang package `ollama` atau `llama.cpp` Android build.
3. Jalankan server lokal di port 11434.
4. Kamera HP mengambil foto komponen mesin/elektronik $\rightarrow$ kirim ke API lokal Android $\rightarrow$ teks diagnosis langsung muncul di layar HP tanpa kuota data!

---

## 3. Menjalankan di Laptop / PC (Windows / Linux / Mac)

Di laptop atau PC Windows/Mac dengan prosesor modern:
1. Pasang [Ollama](https://ollama.com/).
2. Buat file `Modelfile`:
   ```dockerfile
   FROM ./edge-vlm-diag-q4_k_m.gguf
   TEMPLATE """{{ if .System }}<|im_start|>system
   {{ .System }}<|im_end|>
   {{ end }}{{ if .Prompt }}<|im_start|>user
   {{ .Prompt }}<|im_end|>
   {{ end }}<|im_start|>assistant
   """
   PARAMETER temperature 0.2
   PARAMETER stop "<|im_end|>"
   ```
3. Daftarkan model:
   ```bash
   ollama create edge-vlm -f Modelfile
   ollama run edge-vlm
   ```
4. Model siap digunakan secara lokal dengan kecepatan 40-70 token/detik!
