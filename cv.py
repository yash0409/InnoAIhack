import cv2
import mediapipe as mp
import numpy as np

mp_face = mp.solutions.face_mesh

# =========================
# 🔹 FEATURE EXTRACTION
# =========================
def extract_features(frame, landmarks):
    h, w, _ = frame.shape

    points = []
    for lm in landmarks.landmark:
        points.append([lm.x * w, lm.y * h])

    points = np.array(points)

    # Face width & height
    width = np.linalg.norm(points[234] - points[454])
    height = np.linalg.norm(points[10] - points[152])

    ratio = width / height

    brightness = frame.mean()

    return ratio, brightness


# =========================
# 🔹 DOSHA LOGIC
# =========================
def predict_dosha(ratio, brightness):
    vata, pitta, kapha = 0, 0, 0

    # Face shape
    if ratio < 0.75:
        vata += 2
    elif ratio < 0.9:
        pitta += 2
    else:
        kapha += 2

    # Skin tone (approx)
    if brightness > 150:
        pitta += 1
    elif brightness > 110:
        kapha += 1
    else:
        vata += 1

    scores = {"Vata": vata, "Pitta": pitta, "Kapha": kapha}
    dominant = max(scores, key=scores.get)

    return dominant, scores


# =========================
# 🔹 REAL-TIME LOOP
# =========================
cap = cv2.VideoCapture(0)

with mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
) as face_mesh:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:

                ratio, brightness = extract_features(frame, face_landmarks)
                dosha, scores = predict_dosha(ratio, brightness)

                # Display result
                text = f"{dosha} | V:{scores['Vata']} P:{scores['Pitta']} K:{scores['Kapha']}"

                cv2.putText(
                    frame,
                    text,
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Prakriti Detection (Press Q to exit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()