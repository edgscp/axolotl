"""
E2E tests for lora llama
"""

import logging
import os
import tempfile
import unittest
from pathlib import Path

from transformers.utils import is_torch_bf16_gpu_available

from axolotl.cli import load_datasets
from axolotl.common.cli import TrainerCliArgs
from axolotl.train import train
from axolotl.utils.config import normalize_config
from axolotl.utils.dict import DictDefault

LOG = logging.getLogger("axolotl.tests.e2e")
os.environ["WANDB_DISABLED"] = "true"


class TestFusedLlama(unittest.TestCase):
    """
    Test case for Llama models using Fused layers
    """

    def test_fft_packing(self):
        # pylint: disable=duplicate-code
        output_dir = tempfile.mkdtemp()
        cfg = DictDefault(
            {
                "base_model": "JackFram/llama-68m",
                "base_model_config": "JackFram/llama-68m",
                "flash_attention": True,
                "flash_attn_fuse_qkv": True,
                "flash_attn_fuse_mlp": True,
                "sample_packing": True,
                "sequence_len": 1024,
                "val_set_size": 0.1,
                "special_tokens": {
                    "unk_token": "<unk>",
                    "bos_token": "<s>",
                    "eos_token": "</s>",
                },
                "datasets": [
                    {
                        "path": "mhenrichsen/alpaca_2k_test",
                        "type": "alpaca",
                    },
                ],
                "num_epochs": 2,
                "micro_batch_size": 2,
                "gradient_accumulation_steps": 1,
                "output_dir": output_dir,
                "learning_rate": 0.00001,
                "optimizer": "adamw_torch",
                "lr_scheduler": "cosine",
                "max_steps": 20,
                "save_steps": 10,
                "eval_steps": 10,
            }
        )
        if is_torch_bf16_gpu_available():
            cfg.bf16 = True
        else:
            cfg.fp16 = True
        normalize_config(cfg)
        cli_args = TrainerCliArgs()
        dataset_meta = load_datasets(cfg=cfg, cli_args=cli_args)

        train(cfg=cfg, cli_args=cli_args, dataset_meta=dataset_meta)
        assert (Path(output_dir) / "pytorch_model.bin").exists()
