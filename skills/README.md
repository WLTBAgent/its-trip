<!--
Copyright (c) 2025 Southeast University
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

# Skills Directory

This folder contains hot-pluggable agent skills as Markdown files.

Format: Markdown with a YAML front matter header.

Example:

```md
---
name: event-understanding-default
agent: event-understanding
description: Default skill for event understanding.
inputs: [uploaded_file, text]
outputs: [event_text, incident_extract_draft]
resources:
  - trip_ai.resources.ocr_tool.OcrTool
  - SiliconFlow vision
---

## Action Guide
1) Do X...
```

