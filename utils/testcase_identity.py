from __future__ import annotations

import re
import unicodedata


def repair_mojibake(text: str) -> str:
    for source_encoding in ("latin1", "cp1252"):
        try:
            repaired = text.encode(source_encoding).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if repaired != text:
            return repaired
    return text


def decode_escape_sequences(text: str) -> str:
    if "\\x" not in text and "\\u" not in text and "\\U" not in text:
        return text
    try:
        return text.encode("utf-8").decode("unicode_escape")
    except UnicodeDecodeError:
        return text


def normalize_test_text(value: str | None) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    text = decode_escape_sequences(text)
    if any(marker in text for marker in ("Ã", "Ä", "Â", "Æ", "â")):
        text = repair_mojibake(text)
    return text


def canonical_token(value: str | None) -> str:
    normalized = normalize_test_text(value)
    decomposed = unicodedata.normalize("NFKD", normalized)
    without_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", without_marks.lower())

