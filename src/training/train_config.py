"""
Training configuration and hyperparameters for Edge-VLM Fine-Tuning.
Optimized for Google Colab A100 (40GB/80GB) and T4 GPUs.
"""

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ModelArguments:
    base_model_name: str = field(
        default="Qwen/Qwen2-VL-2B-Instruct",
        metadata={"help": "Nama base model dari Hugging Face Hub (misal: Qwen2-VL-2B-Instruct atau SmolVLM-2B)"}
    )
    use_4bit_quantization: bool = field(
        default=True,
        metadata={"help": "Aktifkan kuantisasi 4-bit (BitsAndBytes NormalFloat4) untuk hemat VRAM"}
    )
    lora_r: int = field(
        default=16,
        metadata={"help": "LoRA rank dimension"}
    )
    lora_alpha: int = field(
        default=32,
        metadata={"help": "LoRA scaling alpha"}
    )
    lora_dropout: float = field(
        default=0.05,
        metadata={"help": "LoRA dropout rate"}
    )
    target_modules: List[str] = field(
        default_factory=lambda: [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        metadata={"help": "Modul attention dan MLP yang disuntikkan adapter LoRA"}
    )

@dataclass
class DataArguments:
    dataset_file: str = field(
        default="data/train_sharegpt.json",
        metadata={"help": "Path file dataset berformat JSON ShareGPT"}
    )
    image_folder: str = field(
        default="data/images",
        metadata={"help": "Folder direktori penyimpanan gambar"}
    )
    max_seq_length: int = field(
        default=2048,
        metadata={"help": "Panjang konteks maksimum token percakapan"}
    )

@dataclass
class TrainingHyperparameters:
    output_dir: str = "./checkpoints/edge_vlm_lora"
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.05
    weight_decay: float = 0.01
    lr_scheduler_type: str = "cosine"
    logging_steps: int = 10
    save_strategy: str = "steps"
    save_steps: int = 50
    save_total_limit: int = 2
    fp16: bool = False
    bf16: bool = True  # A100 mendukung Native Bfloat16
    report_to: str = "none"  # "tensorboard" atau "wandb"
