import json
from datasets import Dataset
from huggingface_hub import login

login(token="TOKEN")

INPUT_PATH = "kprofiles_group_data/kprofiles_eval.json"
REPO_NAME = "UlrickBL/kpop-entity-specific-content-eval-pairs"

rows = []

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        question = line.get("question")
        answer = line.get("answer")

        rows.append({
            "question": question,
            "answer": answer,
        })

ds = Dataset.from_list(rows)

ds.push_to_hub(REPO_NAME)
