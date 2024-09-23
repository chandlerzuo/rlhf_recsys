---
base_model: THUDM/glm-4-9b-chat
library_name: peft
license: other
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: amazon_video_games_orpo
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# amazon_video_games_orpo

This model is a fine-tuned version of [THUDM/glm-4-9b-chat](https://huggingface.co/THUDM/glm-4-9b-chat) on the amazon_video_games dataset.
It achieves the following results on the evaluation set:
- Loss: 0.1257
- Rewards/chosen: -0.0033
- Rewards/rejected: -0.0038
- Rewards/accuracies: 0.5600
- Rewards/margins: 0.0006
- Logps/rejected: -0.0381
- Logps/chosen: -0.0326
- Logits/rejected: -1.9697
- Logits/chosen: -1.9700
- Sft Loss: 0.0012
- Odds Ratio Loss: 1.2451

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-06
- train_batch_size: 1
- eval_batch_size: 1
- seed: 42
- gradient_accumulation_steps: 8
- total_train_batch_size: 8
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 3.0

### Training results



### Framework versions

- PEFT 0.12.0
- Transformers 4.44.1
- Pytorch 2.4.1+cu121
- Datasets 2.19.1
- Tokenizers 0.19.1