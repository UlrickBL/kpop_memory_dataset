import json
with open("kprofiles_group_data/kprofiles_groups.jsonl","r") as f :
    for line in f :
        data = json.loads(line)
        break

print(data.keys())