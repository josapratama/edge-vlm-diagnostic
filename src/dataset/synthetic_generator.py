#!/usr/bin/env python3
"""
Synthetic Dataset Generator for Edge-VLM Diagnostic.
Generates structured multimodal QA pairs and formats them for Qwen2-VL / SmolVLM SFT training.
"""

import json
import os
import random
from typing import List, Dict

try:
    from prompt_templates import SYSTEM_PROMPT, CATEGORIES, DIAGNOSTIC_SAMPLE_DATA
except ImportError:
    from .prompt_templates import SYSTEM_PROMPT, CATEGORIES, DIAGNOSTIC_SAMPLE_DATA

HARDWARE_ITEMS = {
    "motorcycle": [
        ("Injektor Bensin Keihin 6-Hole", "Penyumbatan endapan kerak residu BBM pada lubang nozel", "Debit bahan bakar berkurang drastis, mesin brebet di putaran menengah"),
        ("Sensor Suhu Mesin EOT/ECT", "Konektor sensor berkarat hijau akibat oksidasi air cucian", "ECU membaca sinyal resistansi tak terhingga (-40°C), campuran BBM disiram terlalu kaya"),
        ("Koil Pengapian & Tutup Busi", "Isolator karet tutup busi sobek dan kabel tegangan tinggi bocor ke rangka", "Percikan api pengapian bocor saat hujan / kondisi lembap"),
        ("Spull Stator Magnet 3-Phase", "Gulungan tembaga fase ke-2 gosong akibat panas berlebih", "Pengisian aki drop di bawah 12.4V saat mesin berputar, aki tekor berulang"),
        ("Kampas Ganda CVT & Mangkok Kopling", "Permukaan mangkok kopling membiru akibat overheat selip", "Getaran hebat (gredeg) pada tarikan awal motor matic"),
        ("Kiprok / Regulator Rectifier", "Sirip pendingin tertutup lumpur dan soket kabel meleleh", "Tegangan pengisian melonjak melebihi 16V, lampu utama sering putus")
    ],
    "pcb_iot": [
        ("Mikrokontroler STM32F401", "Pin osilator kristal 8MHz memiliki jembatan timah solder mikro", "Mikrokontroler gagal boot up / stuck pada hard fault handler"),
        ("Step-Down Buck Converter MP1584", "Induktor SMD retak intinya dan dioda schottky panas ekstrem", "Tegangan output 5V berfluktuasi liar memicu reset acak pada sensor"),
        ("Modul Transceiver LoRa SX1278", "Konektor antena SMA longgar tanpa ground plane terpasang", "Output RF memantul balik (high VSWR), modul panas dan jangkauan drop drastis"),
        ("Konektor Baterai LiPo JST-PH 2.0", "Pin tembaga terminal bengkok dan longgar di dalam housing", "Drop tegangan mendadak saat board menarik arus puncak WiFi transmission"),
        ("Sensor Gas MQ-135 / BME680", "Membran pelindung sensor tertutup debu oli tebal", "Sensitivitas pembacaan kualitas udara melenceng jauh dari kalibrasi")
    ],
    "drone_uav": [
        ("Motor Brushless 2207 1950KV", "Bearing motor berbunyi kasar dan terdapat pasir halus di dalam bell", "Getaran frekuensi tinggi (gyro noise) yang memicu panas berlebih pada PID loop"),
        ("Flight Controller F405 OSD", "Sensor Gyro MPU6000 terkena percikan timah saat menyolder buzzer", "Drone terbalik seketika (flip of death) saat throttle dinaikkan"),
        ("Kamera FPV Micro HD", "Lensa kamera tergores dalam dan kabel sensor CMOS kendor", "Tampilan video FPV buram dan flickering saat motor mencapai RPM tinggi"),
        ("Propeller Tri-Blade 5 Inch", "Ujung bilah propeller mengalami chip/retak mikroskopis", "Ketidakseimbangan aerodinamis yang memicu osilasi motor dan konsumsi baterai boros")
    ]
}

def generate_sample_record(index: int, image_path: str = None) -> Dict:
    """Generate a single ShareGPT-formatted conversational record."""
    domain = random.choice(list(HARDWARE_ITEMS.keys()))
    comp_name, defect, symptom = random.choice(HARDWARE_ITEMS[domain])
    
    if image_path is None:
        image_path = f"images/{domain}_{index:04d}.jpg"
        
    user_questions = [
        f"Lakukan inspeksi visual pada komponen {comp_name} ini. Jelaskan masalahnya.",
        f"Tolong periksa foto {comp_name} berikut. Apakah ada tanda-tanda kerusakan fisik?",
        f"Diagnosa komponen dalam gambar ini ({comp_name}) dan berikan panduan perbaikannya.",
        f"Sebagai asisten teknisi hardware, analisa kondisi visual {comp_name} pada foto ini."
    ]
    
    response_text = f"""1. 🔍 **Identifikasi Komponen**: {comp_name}.
2. ⚠️ **Temuan Masalah/Anomali**: {defect}.
3. 🧠 **Analisis Akar Penyebab (Root Cause)**: {symptom}. Kondisi ini secara visual terlihat pada integritas fisik komponen yang mengalami degradasi atau instalasi yang kurang presisi.
4. 🛠️ **Rekomendasi Tindakan Perbaikan**:
   - Lakukan pembersihan area komponen menggunakan cairan pembersih khusus (electronic cleaner / contact cleaner).
   - Periksa tegangan kerja dan kontinuitas jalur menggunakan DMM (Digital Multimeter).
   - Lakukan penggantian atau kalibrasi ulang komponen sebelum dioperasikan kembali untuk menjamin keselamatan."""

    return {
        "id": f"hw_diag_{index:06d}",
        "conversations": [
            {
                "from": "human",
                "value": f"<image>\n{random.choice(user_questions)}"
            },
            {
                "from": "gpt",
                "value": response_text
            }
        ],
        "image": image_path,
        "metadata": {
            "domain": domain,
            "component": comp_name
        }
    }

def export_synthetic_dataset(output_path: str, count: int = 500):
    """Export synthetic training records into ShareGPT JSON format."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    records = []
    
    # Masukkan sampel awal manual berkualitas tinggi
    for idx, sample in enumerate(DIAGNOSTIC_SAMPLE_DATA):
        records.append({
            "id": f"seed_{idx:03d}",
            "conversations": [
                {"from": "human", "value": f"<image>\n{sample['instruction']}"},
                {"from": "gpt", "value": sample['response']}
            ],
            "image": f"images/seed_{sample['category']}.jpg",
            "metadata": {"category": sample['category']}
        })
        
    for i in range(len(records), count):
        records.append(generate_sample_record(i))
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Berhasil membuat {len(records)} sampel dataset ShareGPT di: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "train_sharegpt.json")
    export_synthetic_dataset(out_file, count=300)
