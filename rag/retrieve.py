from rag.embed import embed_query

def retrieve(query, store):
    q_emb = embed_query(query)
    docs = store.search(q_emb)
    return docs