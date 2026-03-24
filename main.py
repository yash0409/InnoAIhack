from rag.ingest import load_docs
from rag.embed import embed_texts
from rag.vectorstore import FAISSStore
from rag.retrieve import retrieve
from rag.prompts import build_prompt
from rag.generate import generate

print("🔄 Loading data...")
docs = load_docs()

print("🧠 Creating embeddings...")
embeddings = embed_texts(docs)

dim = len(embeddings[0])
store = FAISSStore(dim)
store.add(embeddings, docs)

print("✅ Ready! Ask your questions (type 'exit' to quit)\n")

while True:
    query = input("🧑 You: ")

    if query.lower() == "exit":
        break

    docs = retrieve(query, store)
    prompt = build_prompt(query, docs)
    response = generate(prompt)

    print("\n🌿 AYUSH AI:\n")
    print(response)
    print("\n" + "-"*50 + "\n")