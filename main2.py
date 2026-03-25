import pickle
import requests

from rag.ingest import load_docs
from rag.embed import embed_texts, embed_query
from rag.vectorstore import FAISSStore
from rag.prompts import build_prompt
from rag.generate import generate

# =========================
# 🔹 LOAD ML MODEL
# =========================
with open(r"D:\InnoAI\ayush-rag-cli\InnoAIhack\dosha_model_v1 (2).pkl", "rb") as f:
    model = pickle.load(f)



def predict_dosha(text):
    pred = model.predict([text])[0]
    probs = model.predict_proba([text])[0]

    confidence = dict(zip(model.classes_, probs))
    return pred, confidence
# =========================
# 🔹 GEO MODULE
# =========================

API_KEY =0


def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    data = requests.get(url).json()

    temp = float(data["current_condition"][0]["temp_C"])
    humidity = int(data["current_condition"][0]["humidity"])

    return temp, humidity


def geo_risk(temp, humidity):
    risks = {}

    risks['Dengue'] = "HIGH" if humidity > 70 and temp > 25 else "LOW"

    if temp > 35:
        risks['Heat Stress'] = "HIGH"
    elif temp > 30:
        risks['Heat Stress'] = "MEDIUM"
    else:
        risks['Heat Stress'] = "LOW"

    risks['Respiratory Issues'] = "MEDIUM" if humidity < 30 else "LOW"

    return risks


def combine_geo_dosha(dosha, risks):
    insights = []

    if dosha == "Pitta" and risks['Heat Stress'] in ["HIGH", "MEDIUM"]:
        insights.append("Higher risk of heat-related imbalance")

    if dosha == "Kapha" and risks['Dengue'] == "HIGH":
        insights.append("Possible congestion-related vulnerability")

    if dosha == "Vata" and risks['Respiratory Issues'] == "MEDIUM":
        insights.append("Vata imbalance may worsen breathing issues")

    return insights


# =========================
# 🔹 BUILD FAISS
# =========================

print("🔄 Loading RAG data...")
docs = load_docs()

print("🧠 Creating embeddings...")
embeddings = embed_texts(docs)

dim = len(embeddings[0])
store = FAISSStore(dim)
store.add(embeddings, docs)

print("✅ System Ready!\n")


# =========================
# 🔹 MAIN LOOP
# =========================

while True:
    query = input("🧑 Enter symptoms (or 'exit'): ")

    if query.lower() == "exit":
        break

    city = input("📍 Enter your city: ")

    # 🔹 ML Prediction
    dosha, confidence = predict_dosha(query)
    confidence_pct = max(confidence.values()) * 100

    # 🔹 Geo Module
    temp, humidity = get_weather(city)
    risks = geo_risk(temp, humidity)
    geo_insights = combine_geo_dosha(dosha, risks)

    # 🔹 RAG Retrieval
    q_emb = embed_query(query)
    retrieved_docs = store.search(q_emb)

    # 🔹 Prompt
    prompt = f"""
User Symptoms: {query}
Predicted Dosha: {dosha} ({confidence_pct:.2f}% confidence)

Location: {city}
Temperature: {temp:.1f}°C
Humidity: {humidity}%

Regional Risks:
{risks}

Geo Insights:
{geo_insights}

Context:
{retrieved_docs}

Give:
- Remedies
- Diet
- Yoga
- Explanation based on dosha + environment

IMPORTANT:
Only use the provided context.
"""

    # 🔹 LLM
    response = generate(prompt)

    # =========================
    # 🔹 OUTPUT
    # =========================

    print("\n" + "="*50)
    print("🌿 AYUSH AI OUTPUT\n")

    print(f"🧠 Dosha: {dosha} ({confidence_pct:.2f}%)")

    print(f"\n📍 Location: {city}")
    print(f"🌡️ Temp: {temp:.1f}°C | 💧 Humidity: {humidity}%")

    print("\n⚠️ Regional Risks:")
    for k, v in risks.items():
        print(f"- {k}: {v}")

    print("\n🧠 Geo Insights:")
    for g in geo_insights:
        print("-", g)

    print("\n💊 Recommendations:\n")
    print(response)

    print("\n" + "="*50 + "\n")