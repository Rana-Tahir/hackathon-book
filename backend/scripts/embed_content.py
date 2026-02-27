"""One-time embedding pipeline: book content → Qdrant vectors.

Usage: python -m scripts.embed_content [--docs-root ../docs]

Compliant with §3.6 Minimal Embeddings Policy:
- 600-token chunks, 50-token overlap
- MD5 hash-based deduplication (skips unchanged chunks)
- Uses fastembed BAAI/bge-small-en-v1.5 (free, local, 384 dims)
- Reports stats for Qdrant Free Tier monitoring
"""

import argparse
import sys
import uuid
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastembed import TextEmbedding
from qdrant_client.http.models import PointStruct

from app.config import settings
from app.services.qdrant import QdrantService, COLLECTION_NAME
from app.services.embedder import discover_chapters, chunk_markdown


def main():
    parser = argparse.ArgumentParser(description="Embed book content into Qdrant")
    parser.add_argument(
        "--docs-root",
        default=str(Path(__file__).resolve().parent.parent.parent / "docs"),
        help="Path to the docs/ directory containing markdown chapters",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report what would be embedded, don't actually embed",
    )
    args = parser.parse_args()

    # Load embedding model (downloaded once, cached locally)
    print("Loading embedding model (BAAI/bge-small-en-v1.5)...")
    embedding_model = TextEmbedding("BAAI/bge-small-en-v1.5")
    print("Model ready.")

    qdrant = QdrantService(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    qdrant.ensure_collection()

    # Discover chapters
    chapters = discover_chapters(args.docs_root)
    print(f"Found {len(chapters)} markdown files")

    # Get existing hashes to skip unchanged content
    existing_hashes: set[str] = set()
    try:
        records, _ = qdrant.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=10000,
            with_payload=["content_hash"],
        )
        existing_hashes = {
            r.payload.get("content_hash", "") for r in records if r.payload
        }
        print(f"Found {len(existing_hashes)} existing embeddings")
    except Exception:
        print("No existing embeddings found (fresh collection)")

    # Collect all new chunks first for batch embedding
    total_chunks = 0
    skipped_chunks = 0
    new_chunk_objects = []

    for ch in chapters:
        content = Path(ch["path"]).read_text(encoding="utf-8")
        chunks = chunk_markdown(content, ch["chapter"], ch["module"])
        for chunk in chunks:
            total_chunks += 1
            if chunk.metadata.content_hash in existing_hashes:
                skipped_chunks += 1
            else:
                new_chunk_objects.append(chunk)

    print(f"New chunks to embed: {len(new_chunk_objects)}")

    if args.dry_run:
        print("\n--- Embedding Pipeline Report ---")
        print(f"Chapters processed: {len(chapters)}")
        print(f"Total chunks: {total_chunks}")
        print(f"Skipped (unchanged): {skipped_chunks}")
        print(f"New embeddings: {len(new_chunk_objects)}")
        print("\n(DRY RUN — no embeddings were actually created)")
        return

    # Embed in batches of 64 (fastembed is optimised for batch processing)
    BATCH = 64
    upserted = 0
    for i in range(0, len(new_chunk_objects), BATCH):
        batch = new_chunk_objects[i : i + BATCH]
        texts = [c.content for c in batch]

        vectors = list(embedding_model.embed(texts))

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=v.tolist(),
                payload={
                    "content": c.content,
                    "module": c.metadata.module,
                    "chapter": c.metadata.chapter,
                    "section": c.metadata.section,
                    "content_type": c.metadata.content_type,
                    "content_hash": c.metadata.content_hash,
                    "position": c.metadata.position,
                },
            )
            for c, v in zip(batch, vectors)
        ]

        qdrant.upsert_points(points)
        upserted += len(points)
        print(f"  [{upserted}/{len(new_chunk_objects)}] Upserted {len(points)} points...")

    print("\n--- Embedding Pipeline Report ---")
    print(f"Chapters processed: {len(chapters)}")
    print(f"Total chunks: {total_chunks}")
    print(f"Skipped (unchanged): {skipped_chunks}")
    print(f"New embeddings: {upserted}")
    print(f"Total in Qdrant: {qdrant.count()}")


if __name__ == "__main__":
    main()
