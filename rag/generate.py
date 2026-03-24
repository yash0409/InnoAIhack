from groq import Groq

client = Groq(
    api_key="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"
)

def generate(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content  