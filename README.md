<!--
Copyright (c) 2025 Southeast University
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

# TRIP - 高速事故工单智能研判

TRIP（Traffic Incident Processing）是一款面向高速公路运营管理场景的智能研判应用。用户可上传事故工单图片/PDF 或输入文本，系统通过多智能体编排依次完成 **事件理解 → 知识调取 → 风险研判 → 方案生成 → 决策下发**，输出结构化事故要素、风险等级、按部门分发的管控措施及可下载的 JSON 结果。

---

## 目录

- [概述](#概述)
- [版本配套](#版本配套)
- [环境准备](#环境准备)
- [源码下载](#源码下载)
- [快速开始](#快速开始)
- [学习教程](#学习教程)
- [目录结构](#目录结构)
- [相关链接](#相关链接)
- [问题反馈](#问题反馈)

---

## 概述

### 核心能力

| 能力 | 说明 |
| --- | --- |
| 多模态输入 | 支持 PNG/JPG/PDF 工单上传，同时可补充文本描述 |
| OCR 解析 | 调用 PaddleOCR `layout-parsing` 接口提取 Markdown 与纯文本 |
| 视觉理解 | 当 OCR 结果过短时，可选调用 SiliconFlow 视觉模型辅助理解 |
| 结构化抽取 | 输出 `IncidentExtract`：时间、路段、桩号、方向、事件类型、伤亡、车道占用等 |
| 风险研判 | 输出 `RiskAssessment`：风险等级 I / II / III / IV / UNKNOWN、置信度、研判原因 |
| 方案生成 | 基于部门职责模板生成 `ControlAction`：责任部门、措施、目标范围、渠道、优先级、建议完成时效 |
| 决策下发 | 按部门聚合为 `dispatch_payloads`，便于对接外部业务系统 |
| 运行历史 | 自动保存运行结果到本地，支持在 UI 中回放与调试 |

### 多智能体流水线

```text
事件理解 (EventUnderstandingAgent)
  → 知识调取 (KnowledgeRetrievalAgent)
  → 风险研判 (RiskAssessmentAgent)
  → 方案生成 (PlanGenerationAgent)
  → 决策下发 (DispatchAgent)
```

每个智能体通过 `GlobalContext` 共享上下文，并在 `traces` 中记录输入摘要、输出摘要、原始模型输出及使用资源，便于审计与问题定位。

---

## 版本配套

| 项目 | 版本/说明 |
| --- | --- |
| Python | ≥ 3.10（代码使用 `\|` 联合类型语法） |
| Streamlit | ≥ 1.36.0 |
| requests | ≥ 2.31.0 |
| pydantic | ≥ 2.7.0 |
| python-dotenv | ≥ 1.0.1 |
| OCR 服务 | PaddleOCR `layout-parsing`（AI Studio 部署） |
| 大模型服务 | OpenAI 兼容接口 `/chat/completions` |
| 默认文本模型 | `Pro/Qwen/Qwen2.5-7B-Instruct`（可通过配置覆盖） |
| 默认视觉模型 | `Qwen/Qwen3.5-27B`（可通过配置覆盖） |

---

##硬件和版本要求

- **产品型号**：香橙派 AI Station（Orange Pi AI Station）
- **AI 处理器**：昇腾 310P（Ascend 310P），10 个 AI Core，主频 1.08GHz，算力 176 TOPS
- **CPU**：16 核，主频 1.9GHz
- **内存**：48GB/96GB LPDDR4X，速率 4266MHz
- **存储**：NVMe SSD 2280 M.2 插槽
- **操作系统**：openEuler 22.03 LTS
- **CANN 版本**：CANN 8.5.0
- **驱动版本**：23.0.rc3
- **Python 版本**：Python 3.9
- **推理框架**：Ollama（本地模型服务）+ MindIE（昇腾推理引擎）

---

## 环境准备

1. **安装 Python 3.10+**

2. **准备 API 密钥或者本地部署**

3. **（可选）准备示例图片**
   仓库已自带 `工单1.png` 与 `事故1.png` 作为默认示例。

---

## 源码下载

```bash
https://gitcode.com/cann/its-trip
```

---

## 快速开始

### 1. 创建虚拟环境并安装依赖

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 配置密钥

复制示例配置文件：

```powershell
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
```

编辑 `.streamlit\secrets.toml`，填入真实密钥：

```toml
PADDLE_OCR_TOKEN = "your_paddle_ocr_token"
SILICONFLOW_API_KEYS = "sk-your-key-1,sk-your-key-2"
```

支持的完整配置项见 `.streamlit/secrets.toml.example`。

### 3. 启动应用

```powershell
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。在页面中上传图片/PDF、填写补充文本，点击 **开始研判** 即可查看结果。

---

## 学习教程

### 上传并研判一次事故工单

1. 打开应用后，点击 **使用默认示例** 加载仓库自带的 `工单1.png` 与 `事故1.png`。
2. 在右侧 **补充文本** 中填写接警补充信息，例如：
   ```text
   现场已封闭第2车道，无人员伤亡，需要拖车。
   ```
3. 点击 **开始研判**，等待多智能体流水线执行完成。
4. 在 **管控下发** 区域查看按部门分发的任务清单，点击 **下载 JSON** 导出完整结果。

### 运行检查器

左侧边栏的 **运行检查器** 会展示每个智能体的原始输出与 trace，便于理解每一步的中间产物。

### 自定义技能（Skills）

`skills/` 目录下的 Markdown 文件支持热插拔。每份技能包含 YAML front matter（名称、所属智能体、输入输出、资源）与 Action Guide。运行时可在左侧边栏选择替换默认技能。详见 [skills/README.md](skills/README.md)。

---

## 目录结构

```text
TRIP/
├── app.py                      # Streamlit 应用入口
├── requirements.txt            # Python 依赖
├── LICENSE                     # Apache 2.0 许可证
├── README.md                   # 本文件
├── CONTRIBUTING.md             # 贡献指南
├── SECURITY.md                 # 安全声明
├── CHANGELOG.md                # 版本变更记录
├── OAT.xml                     # 开源合规扫描配置
├── .pre-commit-config.yaml     # 提交前检查（含 OAT）
├── scripts/
│   └── oat_check.sh            # OAT pre-commit 检查脚本
├── .streamlit/
│   ├── secrets.toml.example    # 密钥配置示例
│   └── secrets.toml            # 真实密钥
├── trip_ai/                    # 核心 Python 包
│   ├── config.py               # 配置读取（secrets/env）
│   ├── schemas.py              # Pydantic 数据模型
│   ├── pipeline.py             # 文本 fallback 与 LLM 调用工具
│   ├── llm_siliconflow.py      # SiliconFlow 客户端
│   ├── ocr_paddle.py           # PaddleOCR 客户端
│   ├── normalize.py            # 输出归一化
│   ├── department_playbook.py  # 部门职责模板
│   ├── skill_loader.py         # Skills 加载器
│   ├── history_store.py        # 运行历史持久化
│   ├── agents/                 # 多智能体实现
│   │   ├── core.py             # Agent/Skill/GlobalContext 定义
│   │   ├── orchestrator.py     # 顺序编排器
│   │   ├── event_understanding.py
│   │   ├── knowledge_retrieval.py
│   │   ├── risk_assessment.py
│   │   ├── plan_generation.py
│   │   └── dispatch.py
│   └── resources/
│       └── ocr_tool.py         # OCR 资源封装
├── skills/                     # 可热插拔的 Agent Skills
│   ├── README.md
│   ├── event_understanding.default.md
│   ├── knowledge_retrieval.default.md
│   ├── risk_assessment.default.md
│   ├── plan_generation.default.md
│   └── dispatch.default.md
└── runs/                       # 本地运行历史
```

---

## 相关链接

- [许可证](LICENSE)
- [贡献指南](CONTRIBUTING.md)
- [安全声明](SECURITY.md)
- [变更记录](CHANGELOG.md)
- [skills 说明](skills/README.md)

---

## 问题反馈

如遇到问题、发现 bug 或有功能建议，欢迎通过以下方式反馈：
zzhou602@seu.edu.cn
