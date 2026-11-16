import json
import os
import chromadb
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Skip audio, TTS, moderation, and terms-gated models
BLOCKED_KEYWORDS = ("whisper", "guard", "tts", "orpheus", "playai", "distil", "compound")

def get_candidate_models() -> list[str]:
    preferred = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "meta-llama/llama-4-maverick-17b-128e-instruct",
        "qwen/qwen3-32b",
        "qwen-qwq-32b",
        "gemma2-9b-it",
        "deepseek-r1-distill-llama-70b",
    ]
    available = [
        m.id for m in client.models.list().data
        if not any(bad in m.id.lower() for bad in BLOCKED_KEYWORDS)
    ]
    ordered = [m for m in preferred if m in available]
    for m in available:
        if m not in ordered:
            ordered.append(m)
    return ordered

def call_groq_json(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Tries active Groq chat models in priority order until one succeeds."""
    last_error = None
    for model_id in get_candidate_models():
        try:
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=temperature,
            )
            return completion.choices[0].message.content
        except Exception as e:
            last_error = e
            continue
    raise RuntimeError(f"All Groq models failed. Last error: {last_error}")

# Cache local embedder so it loads only once
_embedder = None
def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

class LineCritique(BaseModel):
    line_number: int
    original_line: str
    issue_type: str = Field(description="e.g., Forced Rhyme, Broken Meter, Cliche, Weak Verb, Grammar/Punctuation")
    explanation: str
    suggested_rewrite: str

class PoemAnalysis(BaseModel):
    rhyme_scheme: str = Field(description="Exact pattern like ABAB CDCD, AABB, or Free Verse")
    meter_and_rhythm: str = Field(description="Dominant meter (e.g., Iambic Pentameter) and syllable flow notes")
    primary_theme: str = Field(description="1-3 word theme, e.g., Grief & Loss, Nature, Urban Solitude")
    literary_devices_used: list[str] = Field(description="Metaphors, alliteration, enjambment, imagery found")
    overall_score: int = Field(description="Craft score from 1 to 100")
    strengths: str
    line_by_line_mistakes: list[LineCritique]

class BookChapter(BaseModel):
    chapter_number: int
    chapter_title: str
    chapter_epigraph: str = Field(description="A short poetic intro quote written for this section")
    poem_titles: list[str]

class PoetryBookPlan(BaseModel):
    suggested_book_title: str
    subtitle: str
    preface: str = Field(description="A 2-paragraph literary introduction to the poet's collection")
    chapters: list[BookChapter]

def analyze_poem(title: str, content: str) -> tuple[PoemAnalysis, list[dict]]:
    # 1. Retrieve similar dataset poems using local embeddings
    similar_poems = []
    try:
        chroma_client = chromadb.PersistentClient(path="./poetry_chroma_db")
        collection = chroma_client.get_collection(name="classic_poems")
        emb = get_embedder().encode([content])[0].tolist()
        results = collection.query(query_embeddings=[emb], n_results=2)
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            similar_poems.append({
                "title": meta["title"],
                "poet": meta["poet"],
                "excerpt": doc[:300] + "..."
            })
    except Exception:
        pass

    # 2. Analyze poem via Groq Free Tier with strict JSON schema
    schema_json = json.dumps(PoemAnalysis.model_json_schema(), indent=2)
    prompt = f"""
You are a senior poetry editor and prosody expert. Analyze the poem below thoroughly.
Identify the exact rhyme scheme, meter, literary devices, and any technical mistakes (forced rhymes, awkward syllable stress, clichés, punctuation errors, or tense shifts) with concrete line-by-line suggestions.

Return ONLY valid JSON that strictly conforms to this JSON schema:
{schema_json}

Title: {title}
Poem:
{content}
"""
    raw_json = call_groq_json(
        system_prompt="You are a literary editor that responds strictly in valid JSON.",
        user_prompt=prompt,
        temperature=0.2,
    )
    return PoemAnalysis.model_validate_json(raw_json), similar_poems

def generate_book_plan(poems: list[dict], author_name: str) -> PoetryBookPlan:
    poems_summary = "\n\n".join([
        f"Title: {p['title']} (Theme: {p['primary_theme']}, Rhyme: {p['rhyme_scheme']})\n{p['content']}"
        for p in poems
    ])

    schema_json = json.dumps(PoetryBookPlan.model_json_schema(), indent=2)
    prompt = f"""
You are a publishing house editor compiling a debut poetry anthology for author '{author_name}'.
Organize ALL of the following saved poems into thematic chapters, write a cohesive book title, subtitle, chapter epigraphs, and a literary preface.
Every poem title provided must appear in one of the chapters.

Return ONLY valid JSON that strictly conforms to this JSON schema:
{schema_json}

Saved Poems:
{poems_summary}
"""
    raw_json = call_groq_json(
        system_prompt="You are a publishing house editor that responds strictly in valid JSON.",
        user_prompt=prompt,
        temperature=0.4,
    )
    return PoetryBookPlan.model_validate_json(raw_json)