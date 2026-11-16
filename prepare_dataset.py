import chromadb
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

def build_poetry_dataset(limit=200):
    print("Downloading Poetry Foundation dataset from Hugging Face...")
    ds = load_dataset("suayptalha/Poetry-Foundation-Poems", split="train")

    filtered = [
        row for row in ds
        if row.get("Poem") and row.get("Title") and 100 < len(row["Poem"]) < 1500
    ][:limit]

    chroma_client = chromadb.PersistentClient(path="./poetry_chroma_db")
    # Reset collection if switching from Gemini embeddings (different vector dimensions)
    try:
        chroma_client.delete_collection(name="classic_poems")
    except Exception:
        pass
    collection = chroma_client.create_collection(name="classic_poems")

    print("Loading local embedding model (all-MiniLM-L6-v2)...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [
        f"Title: {item['Title']}\nPoet: {item.get('Poet', 'Unknown')}\n\n{item['Poem']}"
        for item in filtered
    ]
    embeddings = embedder.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=[f"poem_{idx}" for idx in range(len(filtered))],
        embeddings=embeddings,
        documents=[item["Poem"] for item in filtered],
        metadatas=[
            {
                "title": str(item["Title"]),
                "poet": str(item.get("Poet", "Unknown")),
                "tags": str(item.get("Tags", "")),
            }
            for item in filtered
        ],
    )

    print(f"Successfully indexed {len(filtered)} poems locally in ChromaDB!")

if __name__ == "__main__":
    build_poetry_dataset()