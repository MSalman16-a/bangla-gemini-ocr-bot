import csv
import json
import tempfile

def make_txt(mcqs):
    out = ""
    for i, q in enumerate(mcqs, 1):
        out += f"\nQ{i}. {q['question']}\n"
        for k, v in q['options'].items():
            out += f"{k}) {v}\n"
        out += f"Answer: {q['answer']}\n"
        out += f"Explanation: {q.get('explanation','')}\n"
    return out

def make_csv(mcqs):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    with open(tmp.name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["question","A","B","C","D","answer","explanation"])
        for q in mcqs:
            writer.writerow([
                q["question"],
                q["options"]["A"],
                q["options"]["B"],
                q["options"]["C"],
                q["options"]["D"],
                q["answer"],
                q.get("explanation","")
            ])
    return tmp.name

def make_json(mcqs):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    with open(tmp.name, "w", encoding="utf-8") as f:
        json.dump(mcqs, f, ensure_ascii=False, indent=2)
    return tmp.name
