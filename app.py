import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pickle
import requests

from rag.ingest import load_docs
from rag.embed import embed_texts, embed_query
from rag.vectorstore import FAISSStore
from rag.generate import generate

# =========================
# 🔹 LOAD MODEL
# =========================
with open(r"D:\InnoAI\ayush-rag-cli\InnoAIhack\dosha_model_v1 (2).pkl", "rb") as f:
    model = pickle.load(f)

# =========================
# 🔹 CV SETUP
# =========================
mp_face = mp.solutions.face_mesh

def extract_features(frame, landmarks):
    h, w, _ = frame.shape
    points = np.array([[lm.x * w, lm.y * h] for lm in landmarks.landmark])

    width = np.linalg.norm(points[234] - points[454])
    height = np.linalg.norm(points[10] - points[152])
    ratio = width / height

    brightness = frame.mean()

    return ratio, brightness


def predict_cv_dosha(ratio, brightness):
    vata = pitta = kapha = 0

    if ratio < 0.75:
        vata += 2
    elif ratio < 0.9:
        pitta += 2
    else:
        kapha += 2

    if brightness > 150:
        pitta += 1
    elif brightness > 110:
        kapha += 1
    else:
        vata += 1

    scores = {"Vata": vata, "Pitta": pitta, "Kapha": kapha}
    return max(scores, key=scores.get), scores


# =========================
# 🔹 ML DOSHA
# =========================
def predict_ml_dosha(text):
    pred = model.predict([text])[0]
    probs = model.predict_proba([text])[0]
    confidence = dict(zip(model.classes_, probs))
    return pred, confidence


# =========================
# 🔹 GEO
# =========================
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    data = requests.get(url).json()

    temp = float(data["current_condition"][0]["temp_C"])
    humidity = int(data["current_condition"][0]["humidity"])
    return temp, humidity


def geo_risk(temp, humidity):
    return {
        "Dengue": "HIGH" if humidity > 70 and temp > 25 else "LOW",
        "Heat Stress": "HIGH" if temp > 35 else "MEDIUM" if temp > 30 else "LOW",
        "Respiratory": "MEDIUM" if humidity < 30 else "LOW"
    }


# =========================
# 🔹 LOAD RAG
# =========================
@st.cache_resource
def load_rag():
    docs = load_docs()
    embeddings = embed_texts(docs)
    store = FAISSStore(len(embeddings[0]))
    store.add(embeddings, docs)
    return store

store = load_rag()

# =========================
# 🔹 UI
# =========================
st.title("🌿 AYUSH AI Assistant")

query = st.text_input("Enter your symptoms")
city = st.text_input("Enter your city")

run_cv = st.checkbox("Use Webcam Prakriti Detection")

cv_dosha = None

# =========================
# 🔹 CV SECTION
# =========================
if run_cv:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        with mp_face.FaceMesh(static_image_mode=True) as face_mesh:
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                ratio, brightness = extract_features(frame, results.multi_face_landmarks[0])
                cv_dosha, _ = predict_cv_dosha(ratio, brightness)

        st.image(frame, channels="BGR")
        st.write("📸 CV Dosha:", cv_dosha)

    cap.release()

# =========================
# 🔹 RUN SYSTEM
# =========================
if st.button("Analyze"):

    ml_dosha, confidence = predict_ml_dosha(query)
    confidence_pct = max(confidence.values()) * 100

    # 🔥 FUSION
    final_dosha = ml_dosha
    if cv_dosha:
        final_dosha = ml_dosha if confidence_pct > 60 else cv_dosha

    temp, humidity = get_weather(city)
    risks = geo_risk(temp, humidity)

    docs = store.search(embed_query(query))

    prompt = f"""
Symptoms: {query}
Dosha: {final_dosha}
Location: {city}
Temp: {temp}, Humidity: {humidity}

Context:
{docs}

Give remedies, diet, yoga, explanation.
"""

    response = generate(prompt)

    # =========================
    # 🔹 OUTPUT UI
    # =========================

    st.subheader("🧠 Dosha")
    st.write(f"{final_dosha} ({confidence_pct:.2f}%)")

    st.subheader("🌍 Environment")
    st.write(f"Temp: {temp}°C, Humidity: {humidity}%")
    st.write(risks)

    st.subheader("💊 Recommendations")
    st.write(response)