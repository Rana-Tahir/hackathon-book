"""One-time embedding pipeline: book content → Qdrant vectors.

Usage: python -m scripts.embed_content [--docs-root ../docs/docs]

Compliant with §3.6 Minimal Embeddings Policy:
- 600-token chunks, 50-token overlap
- MD5 hash-based deduplication (skips unchanged chunks)
- No redundant or duplicate content
- Reports stats for Qdrant Free Tier monitoring
"""

import argparse
import sys
import uuid
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import OpenAI
from qdrant_client.http.models import PointStruct

from app.config import settings
from app.services.qdrant import QdrantService, COLLECTION_NAME
from app.services.embedder import discover_chapters, chunk_markdown


def main():
    parser = argparse.ArgumentParser(description="Embed book content into Qdrant")
    parser.add_argument(
        "--docs-root",
        default=str(Path(__file__).resolve().parent.parent.parent / "docs" / "docs"),
        help="Path to the docs/docs/ directory containing markdown chapters",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report what would be embedded, don't actually embed",
    )
    args = parser.parse_args()

    # Initialize clients
    openai_client = OpenAI(api_key=settings.openai_api_key)
    qdrant = QdrantService(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    qdrant.ensure_collection()

    # Discover chapters
    chapters = discover_chapters(args.docs_root)
    print(f"Found {len(chapters)} markdown files")

    # Get existing hashes to skip unchanged content
    existing_hashes: set[str] = set()
    try:
        # Scroll through existing points to get hashes
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

    # Process chapters
    total_chunks = 0
    skipped_chunks = 0
    new_chunks = 0
    points_batch: list[PointStruct] = []

    for ch in chapters:
        content = Path(ch["path"]).read_text(encoding="utf-8")
        chunks = chunk_markdown(content, ch["chapter"], ch["module"])

        for chunk in chunks:
            total_chunks += 1

            # Skip unchanged chunks (incremental update)
            if chunk.metadata.content_hash in existing_hashes:
                skipped_chunks += 1
                continue

            new_chunks += 1

            if args.dry_run:
                continue

            # Generate embedding
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk.content,
            )
            vector = response.data[0].embedding

            points_batch.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "content": chunk.content,
                        "module": chunk.metadata.module,
                        "chapter": chunk.metadata.chapter,
                        "section": chunk.metadata.section,
                        "content_type": chunk.metadata.content_type,
                        "content_hash": chunk.metadata.content_hash,
                        "position": chunk.metadata.position,
                    },
                )
            )

            # Batch upsert every 50 points
            if len(points_batch) >= 50:
                qdrant.upsert_points(points_batch)
                print(f"  Upserted {len(points_batch)} points...")
                points_batch = []

    # Final batch
    if points_batch:
        qdrant.upsert_points(points_batch)

    # Report
    print("\n--- Embedding Pipeline Report ---")
    print(f"Chapters processed: {len(chapters)}")
    print(f"Total chunks: {total_chunks}")
    print(f"Skipped (unchanged): {skipped_chunks}")
    print(f"New embeddings: {new_chunks}")
    print(f"Total in Qdrant: {qdrant.count()}")

    if args.dry_run:
        print("\n(DRY RUN — no embeddings were actually created)")


if __name__ == "__main__":
    main()
