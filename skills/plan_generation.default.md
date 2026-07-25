<!--
Copyright (c) 2025 Huawei Technologies Co., Ltd.
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

---
name: plan-generation-default
agent: plan-generation
description: 方案生成默认技能：按部门职责模板生成可执行任务清单（派单）。
inputs: [event_text, incident_extract_draft, risk_assessment_partial, playbook_full]
outputs: [risk_assessment_with_actions]
resources:
  - SiliconFlow chat.completions
  - trip_ai.department_playbook.DEPARTMENT_PLAYBOOK
---

## Action Guide
1) 严格遵循 playbook 与硬约束生成 `suggested_actions`（覆盖>=3部门，每部门>=2条）。
2) 每条措施必须含：department、action、priority、channel、target、eta_minutes、rationale。
3) 禁止复述原文整句，输出要任务化/参数化。
4) 严格 JSON；失败则一次修复后重试。

