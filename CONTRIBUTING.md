<!--
Copyright (c) 2025 Southeast University
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

# 贡献指南

感谢你对 TRIP（高速事故工单智能研判）项目的关注！本指南将帮助你快速了解如何参与贡献。

---

## 贡献流程

1. **Fork 仓库**：在 [GitCode 仓库页](https://gitcode.com/cann/its-trip) 点击 **Fork**，将仓库复制到你的账号下。
2. **克隆仓库**：
   ```bash
   git clone https://gitcode.com/<your-username>/its-trip.git
   cd its-trip
   ```
3. **创建分支**：从 `master` 分支切出功能分支，命名建议体现修改意图：
   ```bash
   git checkout -b feature/add-vision-model-switch
   ```
4. **本地开发与验证**：
   - 安装依赖：`pip install -r requirements.txt`
   - 复制并配置密钥：`Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml`
   - 启动应用：`streamlit run app.py`
   - 修改后确保核心流程可正常执行（上传示例 → 开始研判 → 查看结果 → 下载 JSON）。
5. **保持提交信息清晰**：使用中文或英文简要说明本次修改，例如：
   ```text
   feat: 支持多文件上传时合并 OCR 结果
   fix: 修复 RiskAssessment 输出解析失败时未记录 trace 的问题
   docs: 更新 README 中的模型版本说明
   ```
6. **推送并提交 Pull Request**：
   ```bash
   git push origin feature/add-vision-model-switch
   ```
   然后在 GitCode 向 `cann/its-trip` 发起 Pull Request，关联相关 Issue（如有）。
7. **代码审查**：维护者将进行审查，必要时请配合修改。
8. **许可证与文件头**：新增或修改可注释源文件时，应保留 / 补充仓库统一的 CANN-2.0 Copyright 文件头（版权主体为 Southeast University）；`json` / `png` / `toml` 等无法添加注释的文件除外。合规检查见根目录 `OAT.xml` 与 `scripts/oat_check.sh`。

---

## Issue 创建规范

在创建 Issue 前，请先搜索是否已有相似问题。

### Bug 报告模板

- **标题**：以 `[Bug]` 开头，简要描述问题
- **环境信息**：
  - 操作系统
  - Python 版本
  - Streamlit 版本
  - 使用的模型名称
- **复现步骤**：按 1、2、3 列出
- **预期结果** 与 **实际结果**
- **关键日志/报错信息**：注意隐去 API key 等敏感信息
- **输入样例**：可脱敏后的图片/文本，或说明使用了哪个默认示例

### Feature 请求模板

- **标题**：以 `[Feature]` 开头
- **背景与动机**：描述使用场景
- **期望功能**：清晰说明希望新增的能力
- **可能的实现方案**（可选）

### 文档改进

- **标题**：以 `[Docs]` 开头
- 说明文档中错误、缺失或不清晰之处，并建议修改内容

---

## PR 提交规范

### 提交前检查清单

- [ ] 代码符合项目现有风格（使用 `from __future__ import annotations`，类型提示等）
- [ ] 新增依赖已写入 `requirements.txt` 并说明原因
- [ ] 新增配置项已在 `.streamlit/secrets.toml.example` 中给出示例
- [ ] 已通过本地运行验证：`streamlit run app.py` 可正常完成一次研判
- [ ] 敏感信息（API key、token、密码）未写入代码或提交记录
- [ ] 提交信息符合规范

### PR 描述要求

- 说明本次修改的目的与范围
- 关联相关 Issue：`Fixes #123` 或 `Relates to #456`
- 如为功能变更，补充验证方式或截图

### 审查与合并

- 至少一位维护者 review 通过后方可合并
- 合并前请确保无敏感信息泄露、无破坏性变更未在 CHANGELOG 中记录

---

## 代码与 Skill 交付件清单

当你新增或修改功能时，请根据以下清单准备交付件，确保其他开发者与 QA 可以复现与验证。

### 1. 代码交付件

| 交付件 | 必填 | 说明 |
| --- | --- | --- |
| Python 源代码 | 是 | 位于 `trip_ai/` 或 `app.py`，遵循现有模块划分 |
| 类型注解 | 是 | 新函数/类需包含类型提示 |
| 错误处理 | 是 | 对 LLM/OCR 等外部调用增加异常捕获与 trace 记录 |
| 配置示例 | 是 | 新增配置项必须在 `.streamlit/secrets.toml.example` 中示例 |
| 依赖声明 | 条件 | 新增第三方包需写入 `requirements.txt` |

### 2. Skill 交付件（新增/修改智能体行为时）

| 交付件 | 必填 | 说明 |
| --- | --- | --- |
| Skill Markdown | 是 | 位于 `skills/<agent>.<name>.md`，包含 YAML front matter |
| 元数据 | 是 | `name`、`agent`、`description`、`inputs`、`outputs` |
| 资源声明 | 是 | `resources` 中列明使用的工具/模型/数据 |
| Action Guide | 是 | 清晰描述智能体执行步骤与输出约束 |
| 默认 Skill 更新 | 条件 | 若修改默认行为，需同步更新 `*.default.md` |

### 3. 文档交付件

| 交付件 | 必填 | 说明 |
| --- | --- | --- |
| README 更新 | 条件 | 若涉及接口、数据类型、启动方式变更需同步更新 |
| CHANGELOG 更新 | 是 | 记录版本号、变更内容、修复问题 |
| 安全声明更新 | 条件 | 若新增外部网络调用或文件操作需更新 SECURITY.md |

### 4. 验证交付件

| 交付件 | 必填 | 说明 |
| --- | --- | --- |
| 本地运行验证 | 是 | 至少完成一次端到端研判并生成 JSON 结果 |
| 敏感信息检查 | 是 | 确认未提交 `secrets.toml`、日志中的 key 等 |

---

## 行为准则

- 保持友善与尊重，接受建设性反馈
- 聚焦问题本身，避免人身攻击
- 尊重不同观点，通过讨论达成共识

