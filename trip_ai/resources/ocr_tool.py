# Copyright (c) 2025 Southeast University
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings
from ..ocr_paddle import OcrParsed, parse_with_paddle_layout_parsing


@dataclass(frozen=True)
class OcrTool:
    """
    Resource tool used by the Event Understanding agent.
    """

    settings: Settings

    def run(self, *, file_bytes: bytes, filename: str) -> OcrParsed:
        return parse_with_paddle_layout_parsing(settings=self.settings, file_bytes=file_bytes, filename=filename)

