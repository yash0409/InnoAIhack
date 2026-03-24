# =========================
# 🧬 PRAKRITI DETECTION MODULE
# =========================

questions = [
    {
        "q": "How is your body frame?",
        "options": {
            "A": ("Thin, light", "Vata"),
            "B": ("Medium, muscular", "Pitta"),
            "C": ("Heavy, broad", "Kapha")
        }
    },
    {
        "q": "How is your skin?",
        "options": {
            "A": ("Dry, rough", "Vata"),
            "B": ("Warm, oily", "Pitta"),
            "C": ("Soft, moist", "Kapha")
        }
    },
    {
        "q": "How is your digestion?",
        "options": {
            "A": ("Irregular", "Vata"),
            "B": ("Strong, fast", "Pitta"),
            "C": ("Slow", "Kapha")
        }
    },
    {
        "q": "How is your energy level?",
        "options": {
            "A": ("Variable", "Vata"),
            "B": ("High, intense", "Pitta"),
            "C": ("Stable", "Kapha")
        }
    },
    {
        "q": "How do you react to stress?",
        "options": {
            "A": ("Anxious", "Vata"),
            "B": ("Irritated/angry", "Pitta"),
            "C": ("Calm", "Kapha")
        }
    },
    {
        "q": "How is your sleep?",
        "options": {
            "A": ("Light, disturbed", "Vata"),
            "B": ("Moderate", "Pitta"),
            "C": ("Deep, long", "Kapha")
        }
    },
    {
        "q": "How is your appetite?",
        "options": {
            "A": ("Irregular", "Vata"),
            "B": ("Strong", "Pitta"),
            "C": ("Slow", "Kapha")
        }
    },
    {
        "q": "How is your body temperature?",
        "options": {
            "A": ("Cold hands/feet", "Vata"),
            "B": ("Warm/hot body", "Pitta"),
            "C": ("Cool and steady", "Kapha")
        }
    },
    {
        "q": "How do you speak?",
        "options": {
            "A": ("Fast, talkative", "Vata"),
            "B": ("Sharp, clear", "Pitta"),
            "C": ("Slow, calm", "Kapha")
        }
    },
    {
        "q": "How is your memory?",
        "options": {
            "A": ("Quick but forgetful", "Vata"),
            "B": ("Sharp and precise", "Pitta"),
            "C": ("Slow but long-lasting", "Kapha")
        }
    }
]


# =========================
# 🔹 QUIZ FUNCTION
# =========================

def prakriti_quiz():
    scores = {"Vata": 0, "Pitta": 0, "Kapha": 0}

    print("\n🧬 Prakriti Detection Quiz")
    print("-" * 40)

    for q in questions:
        print("\n" + q["q"])
        for key, (text, _) in q["options"].items():
            print(f"{key}. {text}")

        while True:
            ans = input("Choose (A/B/C): ").strip().upper()

            if ans in q["options"]:
                dosha = q["options"][ans][1]
                scores[dosha] += 1
                break
            else:
                print("Invalid input. Please choose A, B, or C.")

    return scores


# =========================
# 🔹 RESULT PROCESSING
# =========================

def get_prakriti_result(scores):
    total = sum(scores.values())

    normalized = {k: v / total for k, v in scores.items()}
    dominant = max(normalized, key=normalized.get)

    return dominant, normalized


# =========================
# 🔹 EXPLANATION
# =========================

def explain_prakriti(dominant):
    explanations = {
        "Vata": "You show traits like variability, dryness, and sensitivity.",
        "Pitta": "You show traits like heat, intensity, and strong digestion.",
        "Kapha": "You show traits like stability, calmness, and slow metabolism."
    }

    return explanations.get(dominant, "")


# =========================
# 🔹 MAIN RUNNER
# =========================

def run_prakriti_module():
    scores = prakriti_quiz()
    dominant, normalized = get_prakriti_result(scores)

    print("\n" + "=" * 40)
    print("🧬 PRAKRITI RESULT\n")

    for k, v in normalized.items():
        print(f"{k}: {v:.2f}")

    print(f"\n👉 Dominant Prakriti: {dominant}")

    print("\n🧠 Explanation:")
    print(explain_prakriti(dominant))

    print("=" * 40 + "\n")

    return dominant, normalized


# =========================
# 🔹 RUN STANDALONE
# =========================

if __name__ == "__main__":
    run_prakriti_module()