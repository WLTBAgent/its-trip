<!--
Copyright (c) 2025 Southeast University
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

---
name: risk-assessment-default
agent: risk-assessment
description: 风险研判默认技能：只输出风险等级与原因，不生成处置措施。
inputs: [event_text, incident_extract_draft, constraints_compact]
outputs: [risk_assessment_partial]
resources:
  - SiliconFlow chat.completions
---

## Action Guide
1) 输入 `event_text` 与 `incident_extract_draft`。
2) 输出 `RiskAssessment`，但 `suggested_actions` 必须是空数组 `[]`。
3) 严格 JSON 输出；若解析/校验失败，执行一次 JSON 修复后重试。

