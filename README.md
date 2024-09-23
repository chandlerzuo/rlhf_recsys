## Prerequisit: install LLaMA-Factory in a different directory
```
with-proxy git clone git://hiyouga/LLaMA-Factory llama_factory
# Set up public key for Github
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
conda activate transformer
with-proxy pip install -e ".[torch,metrics]"
```

## Model training and inference
1. run data_preproc.py to generate training and test data in RLHF format.
1. To train the model, under the LLaMA-Factory directory, run ```CUDA_VISIBLE_DEVICES=6 with-proxy llamafactory-cli train ~/llm_finetune_projects/rlhf_recsys/rlhf_train.yaml```.
1. To run inference, under the LLaMA-Factory directory, run ```CUDA_VISIBLE_DEVICES=2 with-proxy llamafactory-cli api ~/llm_finetune_projects/rlhf_recsys/rlhf_inference.yaml``` to start load the model. This wil load the model in localhost. Then run prediction.py.
