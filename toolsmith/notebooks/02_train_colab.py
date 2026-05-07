# Colab Training Notebook

Convert this `.py` to a notebook for Colab one of two ways:

**Option A (recommended):** open `02_train_colab.py` in Jupyter and "File →
Save As → .ipynb" — cell markers below are jupytext-compatible. Or run:

```bash
pip install jupytext
jupytext --to notebook 02_train_colab.py
```

**Option B:** copy each cell (separated by `# %%` markers) into a new Colab notebook manually.

```python
# %% [markdown]
# # ToolSmith — Train on Colab T4
#
# This notebook trains the LoRA adapter end-to-end on a free Colab T4.
# Wall-clock: ~25 min for 1600-example training set.

# %%
# 1. Install + clone
!pip install -q "transformers>=4.46" "peft>=0.13" "trl>=0.11" "datasets" "accelerate" "bitsandbytes" "wandb" "anthropic"
!git clone https://github.com/<your-username>/toolsmith.git
%cd toolsmith
!pip install -q -e .

# %%
# 2. Authenticate to W&B + HuggingFace
import wandb
wandb.login()

from huggingface_hub import notebook_login
notebook_login()

# %%
# 3. (Optional) regenerate synthetic data — skip if data/ already pushed to repo
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."  # paste yours here

!python -m toolsmith.data.generate --n-train 1600 --n-val 200 --n-test 200

# %%
# 4. Train
!python -m toolsmith.train

# %%
# 5. Evaluate
!python -m toolsmith.eval --adapter ./outputs/lora-adapter

# %%
# 6. Push adapter + tokenizer to the Hub
!huggingface-cli upload <your-username>/toolsmith-qwen2.5-0.5b ./outputs/lora-adapter

# %% [markdown]
# That's it. The model card on the Hub auto-renders the README — copy the
# results table from the printout above into `README.md` and push.
```
