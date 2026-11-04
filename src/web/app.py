#!/usr/bin/env python3
"""
Gradio Interactive Web Application for Edge-VLM Diagnostic.
Deployable directly to Hugging Face Spaces or locally at http://localhost:7860.
"""

import os
import gradio as gr
from PIL import Image

try:
    from src.inference.detector import HardwareDiagnosticVLM
except ImportError:
    try:
        from inference.detector import HardwareDiagnosticVLM
    except ImportError:
        HardwareDiagnosticVLM = None

# Inisialisasi engine jika environment GPU tersedia
engine = None
def get_engine():
    global engine
    if engine is None and HardwareDiagnosticVLM is not None:
        try:
            engine = HardwareDiagnosticVLM()
        except Exception as e:
            print(f"Warning: Engine init failed ({e}), running in demo mock mode.")
    return engine

def analyze_hardware(image, prompt_text):
    if image is None:
        return "⚠️ Silakan unggah foto komponen hardware, PCB, atau mesin motor terlebih dahulu."
        
    eng = get_engine()
    if eng is not None:
        temp_path = "/tmp/temp_diag.jpg" if os.name != "nt" else "temp_diag.jpg"
        image.save(temp_path)
        result = eng.diagnose(temp_path, prompt=prompt_text or "Periksa komponen ini.")
        return result
    else:
        # High quality demo mock output for interactive inspection
        return f"""🔍 **HASIL ANALISIS VISUAL MULTIMODAL (DEMO MODE)**:
---------------------------------------------------------------
1. 🔍 **Identifikasi Komponen**: Board Elektronik / Modul Daya & Mikrokontroler.
2. ⚠️ **Temuan Masalah/Anomali**: Jalur solder pada pin daya utama terindikasi mengalami oksidasi ringan dan salah satu kapasitor filter SMD menunjukkan perubahan warna (discoloration).
3. 🧠 **Analisis Akar Penyebab (Root Cause)**: Paparan suhu tinggi berkelanjutan dan fluktuasi riak arus (ripple current) dari sumber power supply.
4. 🛠️ **Rekomendasi Tindakan Perbaikan**:
   - Ukur nilai tegangan ripple menggunakan osiloskop atau multimeter true-RMS.
   - Bersihkan area board dengan Isopropyl Alcohol (IPA 99%).
   - Solder ulang titik kaki komponen dengan timah Sn63/Pb37 berkualitas tinggi."""

# Gradio Interface
custom_css = """
.gradio-container { font-family: 'Segoe UI', system-ui, sans-serif; }
#header-title { text-align: center; margin-bottom: 20px; }
"""

with gr.Blocks(css=custom_css, title="Edge-VLM Hardware Diagnostic") as demo:
    gr.Markdown(
        """
        # 🔬 Edge-VLM Hardware & Automotive Diagnostic
        ### Multimodal Vision-Language Model untuk Inspeksi Visual Mesin Motor, PCB, IoT & Drone
        *Model: Fine-Tuned Qwen2-VL-2B-Instruct dengan Visual Chain-of-Thought (CoT) Reasoning.*
        """,
        elem_id="header-title"
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(type="pil", label="📸 Unggah Foto Komponen / Kerusakan")
            user_prompt = gr.Textbox(
                label="💬 Pertanyaan / Instruksi Teknis",
                placeholder="Contoh: Periksa throttle body dan soket TPS ini...",
                value="Periksa komponen pada foto ini. Apakah ada kerusakan fisik atau anomali?"
            )
            btn_submit = gr.Button("⚡ Mulai Analisis Diagnostik", variant="primary")
            
        with gr.Column(scale=1):
            output_text = gr.Markdown(label="📋 Hasil Diagnostik Multimodal")
            
    btn_submit.click(
        fn=analyze_hardware,
        inputs=[input_image, user_prompt],
        outputs=[output_text]
    )
    
    gr.Markdown("---")
    gr.Markdown("⚡ **Edge-VLM Project Portfolio** | 100% Open Source | Siap di-deploy ke Raspberry Pi 5 & Android")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
