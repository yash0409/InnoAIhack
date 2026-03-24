import json

def load_docs(path="data/ayush_rag_dataset.json"):
    with open(path) as f:
        data = json.load(f)

    docs = []
    for item in data:
        text = f"""
Condition: {item['condition']}
Dosha: {item['dosha']}
Symptoms: {', '.join(item['symptoms'])}
Remedies: {', '.join(item['remedies'])}
Diet: {', '.join(item['diet'])}
Yoga: {', '.join(item['yoga'])}
Explanation: {item['explanation']}
"""
        docs.append(text.strip())

    return docs