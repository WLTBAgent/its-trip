# Copyright (c) 2025 Southeast University
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

from __future__ import annotations

import base64
import os
from dataclasses import dataclass

import requests

from .config import Settings


@dataclass(frozen=True)
class OcrParsed:
    markdown: str
    plain_text: str
    raw: dict


def _guess_file_type(filename: str) -> int:
    """
    PaddleOCR layout-parsing: PDF=0, images=1.
    """
    ext = os.path.splitext(filename.lower())[1]
    if ext == ".pdf":
        return 0
    return 1


def _markdown_to_text(md: str) -> str:
    # A lightweight conversion: strip code fences and markdown syntax crudely.
    # Good enough for LLM prompting; keep original markdown in the record.
    lines: list[str] = []
    for line in md.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("```"):
            continue
        # Drop headings/bullets markers.
        s = s.lstrip("#").lstrip("*").lstrip("-").strip()
        lines.append(s)
    return "\n".join(lines).strip()


def parse_with_paddle_layout_parsing(
    *,
    settings: Settings,
    file_bytes: bytes,
    filename: str,
    use_doc_orientation_classify: bool = False,
    use_doc_unwarping: bool = False,
    use_chart_recognition: bool = False,
) -> OcrParsed:
    if not settings.paddle_ocr_token:
        raise RuntimeError("Missing PADDLE_OCR_TOKEN (set in .streamlit/secrets.toml or env var).")

    file_data = base64.b64encode(file_bytes).decode("ascii")
    file_type = _guess_file_type(filename)

    headers = {
        "Authorization": f"token {settings.paddle_ocr_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "file": file_data,
        "fileType": file_type,
        "useDocOrientationClassify": use_doc_orientation_classify,
        "useDocUnwarping": use_doc_unwarping,
        "useChartRecognition": use_chart_recognition,
    }

    resp = requests.post(settings.paddle_ocr_api_url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    raw = resp.json()
    result = raw.get("result") or {}
    lprs = result.get("layoutParsingResults") or []
    if not lprs:
        return OcrParsed(markdown="", plain_text="", raw=raw)

    # MVP: take the first document.
    md = (lprs[0].get("markdown") or {}).get("text") or ""
    plain = _markdown_to_text(md)
    return OcrParsed(markdown=md, plain_text=plain, raw=raw)

