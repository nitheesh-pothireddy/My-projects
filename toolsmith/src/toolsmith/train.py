"""LoRA SFT training entry-point.

Defaults are tuned for a single Colab T4 (free tier).

Usage:
    python -m toolsmith.train

What this does:
    1. Load Qwen2.5-0.5B-Instruct + tokenizer.
    2. Wrap with PEFT LoRA adapters (q/k/v/o projections).
    3. Load + format JSONL splits via toolsmith.data.format.
    4. Train with TRL's SFTTrainer; log everything to W&B.
    5. Save the adapter to settings.output_dir.
"""

from __future__ import annotations

from pathlib import Path

from toolsmith.config import settings


def main() -> None:
    """Top-level training routine.

    Implementation guide:
        from datasets import Dataset
        from peft import LoraConfig, get_peft_model
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from trl import SFTConfig, SFTTrainer
        import wandb

        wandb.init(project="toolsmith", config=settings.model_dump())

        tokenizer = AutoTokenizer.from_pretrained(settings.base_model)
        model = AutoModelForCausalLM.from_pretrained(
            settings.base_model, torch_dtype="auto", device_map="auto"
        )

        lora_cfg = LoraConfig(
            r=settings.lora_r,
            lora_alpha=settings.lora_alpha,
            lora_dropout=settings.lora_dropout,
            target_modules=settings.lora_target_modules,
            bias="none",
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, lora_cfg)
        model.print_trainable_parameters()  # great line to screenshot for the README

        from toolsmith.data.format import load_jsonl, format_for_sft
        train_rows = format_for_sft(load_jsonl(settings.data_dir / "train.jsonl"), tokenizer)
        val_rows   = format_for_sft(load_jsonl(settings.data_dir / "val.jsonl"),   tokenizer)
        train_ds, val_ds = Dataset.from_list(train_rows), Dataset.from_list(val_rows)

        trainer = SFTTrainer(
            model=model,
            args=SFTConfig(
                output_dir=str(settings.output_dir),
                num_train_epochs=settings.epochs,
                per_device_train_batch_size=settings.batch_size,
                gradient_accumulation_steps=settings.grad_accum,
                learning_rate=settings.lr,
                warmup_ratio=settings.warmup_ratio,
                logging_steps=10,
                eval_strategy="steps",
                eval_steps=50,
                save_strategy="epoch",
                bf16=True,
                report_to="wandb",
                seed=settings.seed,
                max_seq_length=settings.max_seq_length,
            ),
            train_dataset=train_ds,
            eval_dataset=val_ds,
            tokenizer=tokenizer,
        )

        trainer.train()
        trainer.save_model(str(settings.output_dir / "lora-adapter"))
        tokenizer.save_pretrained(str(settings.output_dir / "lora-adapter"))
    """
    Path(settings.output_dir).mkdir(parents=True, exist_ok=True)
    raise NotImplementedError(
        "Implement train.main() — full guide is in the docstring above."
    )


if __name__ == "__main__":
    main()
