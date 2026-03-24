def build_prompt(query, docs):
    context = "\n\n".join(docs)

    return f"""
You are an expert in Ayurveda.

User Query:
{query}

Context:
{context}

Give:
1. Remedies
2. Diet
3. Yoga
4. Explanation (based on dosha)
"""