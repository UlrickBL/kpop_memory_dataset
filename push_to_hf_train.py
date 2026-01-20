import json
from datasets import Dataset
from huggingface_hub import login

login(token="TOKEN")

INPUT_PATH = "kprofiles_group_data/kprofiles_groups.jsonl"
REPO_NAME = "UlrickBL/kpop-entity-specific-content"

rows = []

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        group = obj.get("group")
        url = obj.get("url")

        for sec in obj.get("sections", []):
            title = sec.get("section_title")
            content = sec.get("content")

            if not content or not title:
                continue

            rows.append({
                "group": group,
                "url": url,
                "section": title.strip(),
                "text": content.strip(),
            })

print(f"Flattened into {len(rows)} rows")

ds = Dataset.from_list(rows)

ds.push_to_hub(REPO_NAME)
