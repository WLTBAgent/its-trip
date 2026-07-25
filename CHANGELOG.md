<!--
Copyright (c) 2025 Huawei Technologies Co., Ltd.
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

# 变更记录

本文件记录 TRIP 项目每个版本的变更内容。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

---

## [Unreleased]

### Added

- 补充开源合规文档：`LICENSE`、`CONTRIBUTING.md`、`SECURITY.md`、`CHANGELOG.md`。
- 重写 `README.md`，增加概述、版本配套、环境准备、源码下载、学习教程、目录结构、相关链接与问题反馈入口。
- 为源码与文档补充 Huawei/CANN 2.0 风格 Copyright 头。
- 新增 `OAT.xml` 开源合规扫描配置，以及 `.pre-commit-config.yaml` + `scripts/oat_check.sh`。

---

## [0.1.0] - 2026-07-21

### Added

- 初始化 TRIP 高速事故工单智能研判 MVP。
- 基于 Streamlit 的单页应用入口 `app.py`。
- 多智能体编排流水线：事件理解 → 知识调取 → 风险研判 → 方案生成 → 决策下发。
- `trip_ai/agents/`：
  - `EventUnderstandingAgent`：OCR 解析 + 视觉补充 + 结构化要素草稿抽取
  - `KnowledgeRetrievalAgent`：部门职责模板与硬约束压缩
  - `RiskAssessmentAgent`：风险等级与研判原因
  - `PlanGenerationAgent`：按部门生成可执行管控措施
  - `DispatchAgent`：按部门聚合为 dispatch_payloads
- `trip_ai/schemas.py`：定义 `IncidentExtract`、`RiskAssessment`、`ControlAction`、`PipelineResult` 等 Pydantic 模型。
- `trip_ai/llm_siliconflow.py`：硅基流动 SiliconFlow OpenAI 兼容客户端，支持多 key 轮询与重试。
- `trip_ai/ocr_paddle.py` / `resources/ocr_tool.py`：PaddleOCR layout-parsing 调用封装。
- `trip_ai/skill_loader.py`：支持热插拔的 Markdown Skills 加载器。
- `trip_ai/history_store.py`：本地运行历史保存与回放。
- `skills/`：默认 Skills 与使用说明。
- 默认示例图片：`工单1.png`、`事故1.png`。
- 配置文件示例 `.streamlit/secrets.toml.example`。

### Notes

- 当前版本为演示/原型阶段，模型生成的管控建议需人工复核后方能用于真实业务系统。
- 默认 OCR 服务地址与大模型地址为示例/第三方服务，生产环境请替换为私有化或授权服务。

---

## 版本号说明

本项目采用语义化版本 [SemVer](https://semver.org/lang/zh-CN/)：

- `MAJOR`：不兼容的 API 或数据模型变更
- `MINOR`：向下兼容的功能新增
- `PATCH`：向下兼容的问题修复
