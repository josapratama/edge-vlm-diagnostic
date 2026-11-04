#!/usr/bin/env python3
"""
Inference Engine for Edge-VLM Diagnostic.
Analyzes hardware, PCB, and automotive images and generates diagnostic reasoning.
"""

import os
import torch
from PIL import Image
from typing import Optional

try:
    from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
    from peft import PeftModel
except ImportError:
    pass

class HardwareDiagnosticVLM:
    def __init__(self, base_model_path: str = "Qwen/Qwen2-VL-2B-Instruct", lora_adapter_path: Optional[str] = None):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"⚡ Inisialisasi Edge-VLM Inference Engine pada: {self.device.upper()}")
        
        self.processor = AutoProcessor.from_pretrained(base_model_path)
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )
        
        if lora_adapter_path and os.path.exists(lora_adapter_path):
            print(f"🔗 Memuat Fine-Tuned LoRA Adapter dari: {lora_adapter_path}")
            self.model = PeftModel.from_pretrained(self.model, lora_adapter_path)
            
        self.model.eval()
        print("✅ Model siap menerima gambar!")

    def diagnose(self, image_path: str, prompt: str = "Periksa komponen ini dan deteksi apakah ada kerusakan fisik atau anomali.") -> str:
        """Run multimodal visual reasoning on an image."""
        if not os.path.exists(image_path):
            return f"❌ Error: File gambar {image_path} tidak ditemukan."
            
        image = Image.open(image_path).convert("RGB")
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        text_prompt = self.processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = self.processor(
            text=[text_prompt],
            images=[image],
            padding=True,
            return_tensors="pt"
        ).to(self.device)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
                top_p=0.9
            )
            
        generated_ids = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, output_ids)
        ]
        response = self.processor.batch_decode(
            generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )[0]
        
        return response

if __name__ == "__main__":
    print("Inference engine module ready. Import and instantiate HardwareDiagnosticVLM.")
