#!/usr/bin/env python3
"""
End-to-End Fine-Tuning Pipeline for Edge-VLM Diagnostic.
Runs on Google Colab A100 / T4 or any local GPU workstation.
"""

import os
import sys
import json
import torch
from dataclasses import asdict
from PIL import Image

try:
    from transformers import (
        Qwen2VLForConditionalGeneration,
        AutoProcessor,
        TrainingArguments,
        Trainer,
        BitsAndBytesConfig
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
except ImportError:
    pass

try:
    from train_config import ModelArguments, DataArguments, TrainingHyperparameters
except ImportError:
    from .train_config import ModelArguments, DataArguments, TrainingHyperparameters

def format_data_for_qwen(json_file: str, processor, max_samples: int = 1000):
    """Load ShareGPT JSON and convert to Qwen2-VL conversational format."""
    if not os.path.exists(json_file):
        print(f"⚠️ File dataset {json_file} tidak ditemukan. Membuat dummy sample...")
        return []
        
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    formatted_dataset = []
    for item in data[:max_samples]:
        convs = item.get("conversations", [])
        if len(convs) < 2:
            continue
            
        user_text = convs[0]["value"].replace("<image>\n", "").strip()
        assistant_text = convs[1]["value"].strip()
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": user_text}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": assistant_text}
                ]
            }
        ]
        formatted_dataset.append(messages)
        
    return formatted_dataset

def main():
    model_args = ModelArguments()
    data_args = DataArguments()
    train_args = TrainingHyperparameters()
    
    print("=" * 60)
    print("🚀 Inisialisasi Fine-Tuning Edge-VLM Hardware Diagnostic")
    print(f"📦 Base Model: {model_args.base_model_name}")
    print(f"⚡ Device: {'CUDA (GPU)' if torch.cuda.is_available() else 'CPU'}")
    if torch.cuda.is_available():
        print(f"🎮 GPU Device Name: {torch.cuda.get_device_name(0)}")
        print(f"🧠 Total VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
    print("=" * 60)
    
    # 1. Konfigurasi Kuantisasi BitsAndBytes (4-Bit NF4)
    bnb_config = None
    if model_args.use_4bit_quantization and torch.cuda.is_available():
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16 if train_args.bf16 else torch.float16
        )
        print("✅ 4-Bit NormalFloat Quantization Aktif (Hemat VRAM)")

    # 2. Muat Processor & Tokenizer
    print("⏳ Memuat Processor & Image Tokenizer...")
    processor = AutoProcessor.from_pretrained(
        model_args.base_model_name,
        min_pixels=256 * 28 * 28,
        max_pixels=1280 * 28 * 28
    )

    # 3. Muat Base Model
    print("⏳ Memuat Model Weights...")
    device_map = "auto" if torch.cuda.is_available() else None
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_args.base_model_name,
        quantization_config=bnb_config,
        device_map=device_map,
        torch_dtype=torch.bfloat16 if train_args.bf16 else torch.float16
    )

    # 4. Konfigurasi LoRA Adapter
    print("⏳ Menyiapkan LoRA Adapter...")
    if model_args.use_4bit_quantization:
        model = prepare_model_for_kbit_training(model)
        
    peft_config = LoraConfig(
        r=model_args.lora_r,
        lora_alpha=model_args.lora_alpha,
        lora_dropout=model_args.lora_dropout,
        target_modules=model_args.target_modules,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    print("\n✅ Model dan LoRA Adapter siap untuk proses training!")
    print(f"📁 Checkpoint akan disimpan di: {train_args.output_dir}")

if __name__ == "__main__":
    main()
