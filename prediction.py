import json
import os
from openai import OpenAI
from tqdm import tqdm

data_dir = "/data/users/chandlerzuo/llm_finetune_projects/rlhf_recsys"
api_host = os.environ.get("API_HOST", "0.0.0.0")

# Load OpenAI API
client = OpenAI(
    api_key="EMPTY",
    base_url=f"http://{api_host}:8000/v1/"
)

# Load the test data
test_file_path = f"{data_dir}/processed/rlhf_test.json"
with open(test_file_path, "r", encoding='utf-8') as test_file:
    test_data = json.load(test_file)
print(len(test_data))

# Start running prediction
labels = []
predictions = []
cc = 0
for each_test in tqdm(test_data):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": each_test["instruction"]
            },
            {
                "role": "user",
                "content": each_test["input"],
            }
        ],
        model="glm4",
    )

    predictions.append(chat_completion.choices[0].message.content)
    labels.append(each_test["chosen"])

    if len(labels) % 100 == 0:
        correct = 0
        wrong = 0

        for l, p in zip(labels, predictions):
            l = l.strip()
            p = p.strip()
            # print(f'l: {l}, p: {p}')
            
            if l == p:
                correct += 1
            else:
                wrong += 1
                # print(f'\nl: {l}, \np: {p}')
        print(f'Sample size: {len(labels)}, correct: {correct}, incorrect: {wrong}, accuracy: {correct / len(labels)}')
    cc += 1
    
    # if cc > 100:
    #     break

assert len(predictions) == len(labels)

correct = 0
wrong = 0

for l, p in zip(labels, predictions):
    l = l.strip()
    p = p.strip()
    if l == p:
        correct += 1
    else:
        wrong += 1
print(f'Sample size: {len(labels)}, correct: {correct}, incorrect: {wrong}, accuracy: {correct / len(labels)}')
