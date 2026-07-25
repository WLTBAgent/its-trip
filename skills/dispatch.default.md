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
name: dispatch-default
agent: dispatch
description: 决策下发默认技能：把分部门任务清单整理为对接 payload 草稿（不做真实对接）。
inputs: [risk_assessment_with_actions]
outputs: [dispatch_payloads]
resources: []
---

## Action Guide
1) 按 `department` 分组任务清单。
2) 生成每部门一个 `dispatch_payload`（包含任务列表与风险等级）。
3) 不调用外部系统，仅产出可对接结构。

