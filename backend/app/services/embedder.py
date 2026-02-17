"""Text chunking and embedding service for book content (§3.6 compliant)."""

import hashlib
import os
import re
from pathlib import Path

from app.models.embedding import EmbeddingChunk, EmbeddingMetadata

# Module mapping based on directory names
MODULE_MAP = {
    "module-1": 1,
    "module-2": 2,
    "module-3": 3,
    "module-4": 4,
    "capstone": 4,  # Capstone is part of Module 4 scope
    "appendix": 0,  # Appendix is module 0 (general)
}

TARGET_CHUNK_SIZE = 600  # tokens (target, within 500-800 range)
OVERLAP_SIZE = 50  # tokens


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English."""
    return len(text) // 4


def _compute_hash(text: str) -> str:
    """MD5 hash for content deduplication."""
    return hashlib.md5(text.encode()).hexdigest()


def _strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from markdown."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].strip()
    return content


def _extract_section(text: str) -> str:
    """Extract the most recent heading as the section name."""
    lines = text.strip().split("\n")
    for line in lines:
        if line.startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip()
    return "Introduction"


def _detect_content_type(text: str) -> str:
    """Detect whether a chunk is prose, code, table, or definition."""
    code_lines = sum(1 for line in text.split("\n") if line.startswith("```"))
    table_lines = sum(1 for line in text.split("\n") if "|" in line and "---" in line)

    if code_lines >= 2:
        return "code"
    if table_lines >= 2:
        return "table"
    if text.strip().startswith("**") and ":" in text[:100]:
        return "definition"
    return "prose"


def chunk_markdown(content: str, chapter: str, module: int) -> list[EmbeddingChunk]:
    """Split markdown content into chunks of ~600 tokens with 50-token overlap."""
    content = _strip_frontmatter(content)

    # Split by paragraphs (double newline)
    paragraphs = re.split(r"\n\n+", content)

    chunks: list[EmbeddingChunk] = []
    current_chunk = ""
    current_section = "Introduction"
    position = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Track current section heading
        if para.startswith("#"):
            current_section = re.sub(r"^#+\s*", "", para).strip()

        # Skip very small code-only blocks that add no educational value
        if para.startswith("```") and _estimate_tokens(para) < 20:
            continue

        candidate = (current_chunk + "\n\n" + para).strip() if current_chunk else para

        if _estimate_tokens(candidate) > TARGET_CHUNK_SIZE + 100:
            # Current chunk is full, emit it
            if current_chunk:
                content_type = _detect_content_type(current_chunk)
                # Skip pure code chunks (§3.6: avoid embedding unnecessary code)
                if content_type != "code" or _estimate_tokens(current_chunk) > 100:
                    chunks.append(
                        EmbeddingChunk(
                            content=current_chunk,
                            metadata=EmbeddingMetadata(
                                module=module,
                                chapter=chapter,
                                section=current_section,
                                content_type=content_type,
                                content_hash=_compute_hash(current_chunk),
                                position=position,
                            ),
                        )
                    )
                    position += 1

            # Start new chunk with overlap from end of previous
            if current_chunk:
                overlap_text = current_chunk[-OVERLAP_SIZE * 4:]  # ~50 tokens
                current_chunk = overlap_text + "\n\n" + para
            else:
                current_chunk = para
        else:
            current_chunk = candidate

    # Emit final chunk
    if current_chunk and _estimate_tokens(current_chunk) > 30:
        content_type = _detect_content_type(current_chunk)
        if content_type != "code" or _estimate_tokens(current_chunk) > 100:
            chunks.append(
                EmbeddingChunk(
                    content=current_chunk,
                    metadata=EmbeddingMetadata(
                        module=module,
                        chapter=chapter,
                        section=current_section,
                        content_type=content_type,
                        content_hash=_compute_hash(current_chunk),
                        position=position,
                    ),
                )
            )

    return chunks


def discover_chapters(docs_root: str) -> list[dict]:
    """Find all markdown chapter files in the docs directory."""
    docs_path = Path(docs_root)
    chapters = []

    for md_file in sorted(docs_path.rglob("*.md")):
        rel_path = md_file.relative_to(docs_path)
        parts = rel_path.parts

        # Determine module from directory
        module = 0
        if len(parts) >= 2:
            dir_name = parts[0]
            module = MODULE_MAP.get(dir_name, 0)
        elif parts[0] == "index.md":
            module = 0

        chapters.append(
            {
                "path": str(md_file),
                "chapter": str(rel_path).replace(".md", ""),
                "module": module,
            }
        )

    return chapters
