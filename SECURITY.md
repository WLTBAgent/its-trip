<!--
Copyright (c) 2025 Huawei Technologies Co., Ltd.
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

# 安全声明

本文档说明 TRIP 项目在运行、构建与日常维护过程中的安全建议、文件权限控制、外部网络地址使用情况及漏洞反馈机制。

---

## 运行用户建议

### 1. 密钥管理

- **不要将真实密钥写入代码或提交到仓库**。本项目通过 `.streamlit/secrets.toml` 或环境变量读取密钥。
- 生产环境建议使用环境变量或 Secrets Manager，而非本地文件。

### 2. 输入数据

- 本项目处理的图片/PDF/文本可能包含事故现场、车牌、人员等敏感信息。请遵守所在组织的数据脱敏与隐私保护规定。
- 运行历史默认保存在本地 `runs/` 目录（已加入 `.gitignore`），请根据安全策略决定是否开启或定期清理。

### 3. 部署建议

- **本地开发**：仅在受信任的内网环境启动
- **公网部署**：建议通过反向代理（Nginx/Traefik）开启 HTTPS，并配置访问控制（如 OAuth、IP 白名单）。
- **不要以 root 用户运行本应用**，建议创建专用低权限账户。

### 4. 日志与 Trace

- 智能体 trace 可能包含原始模型输出片段，其中或存在输入文本。分享日志前请脱敏。
- 日志文件路径 `*.log` 已加入 `.gitignore`，避免泄露敏感信息。

---

## 文件权限控制

### 密钥与配置

| 文件/目录 | 建议权限 | 说明 |
| --- | --- | --- |
| `.streamlit/secrets.toml` | `600`（仅所有者可读写） | 包含 API token 与 key，必须限制访问 |
| `.streamlit/secrets.toml.example` | `644` | 示例文件，不含真实密钥 |
| `runs/` | `700` | 本地运行历史，可能含敏感输入 |
| `output/` | `700` | 输出目录，按需限制 |
| `.venv/` | `755` | Python 虚拟环境 |

### 源代码

| 文件/目录 | 建议权限 | 说明 |
| --- | --- | --- |
| `app.py`、`trip_ai/`、`skills/` | `644` | 源代码只读 |
| `.git/` | `700` | Git 元数据 |

> 在 Windows 环境下，可通过文件属性 → 安全选项卡限制对 `.streamlit/secrets.toml` 的访问。

---

## 构建/运行安全声明

### 依赖安全

- 安装依赖前请确认 `requirements.txt` 中的包来源可信，优先使用官方 PyPI 镜像：
  ```powershell
  pip install -r requirements.txt
  ```
- 建议定期执行 `pip list --outdated` 并关注关键依赖（streamlit、requests、pydantic）的安全公告。

### 外部服务调用

- 运行时会向以下外部地址发起 HTTPS 请求：
  - PaddleOCR `layout-parsing` 服务地址（默认 `https://42n9f1c9u9yci9dd.aistudio-app.com/layout-parsing`，可在配置中覆盖）
  - API（默认 `https://api.siliconflow.cn/v1/chat/completions`，可在配置中覆盖）
- 所有外部调用均通过 `requests` 库使用 TLS，不会以明文传输密钥。
- 若在内网或离线环境使用，需自行部署对应 OCR 与 LLM 服务并修改配置地址。

### 运行时行为

- 应用默认监听 `localhost:8501`，不会主动暴露到公网。
- 若使用 `streamlit run app.py --server.address 0.0.0.0`，请确保已配置防火墙与访问控制。
- 应用不会主动写入系统目录，仅在 `runs/`、`output/` 及当前工作目录下产生文件。

---

## 公网地址声明表

| 地址 | 用途 | 是否可配置 | 是否涉及敏感数据上传 |
| --- | --- | --- | --- |
| `https://42n9f1c9u9yci9dd.aistudio-app.com/layout-parsing` | PaddleOCR 图文解析 | 是（`PADDLE_OCR_API_URL`） | 是（上传图片/PDF） |
| `https://api.siliconflow.cn/v1/chat/completions` | 大模型对话接口 | 是（`SILICONFLOW_BASE_URL`） | 是（OCR 文本/补充文本） |

> 以上默认地址均为示例/演示用途，生产环境请替换为你自己部署或授权使用的服务地址。

---

## 漏洞机制说明

### 已知风险与缓解措施

| 风险点 | 说明 | 缓解措施 |
| --- | --- | --- |
| API key 泄露 | 密钥写入代码或误提交 | 使用 `.streamlit/secrets.toml` 或环境变量；已加入 `.gitignore` |
| 输入数据泄露 | 运行历史保存敏感图片/文本 | `runs/` 已加入 `.gitignore`；按策略清理或禁用持久化 |
| 公网暴露 | 默认仅监听 localhost | 手动配置 `0.0.0.0` 时配合防火墙与 HTTPS |
| 外部服务不可控 | 调用第三方 OCR/LLM | 使用 HTTPS；生产环境建议私有化部署 |
| 提示词注入 | 用户输入可能影响模型输出 | 当前为演示系统，生产环境应增加输入校验与输出审核 |

### 安全边界

- 本项目为研判演示系统，不直接对接真实交通控制系统。
- 任何由模型生成的管控建议均需人工复核后方能下发执行。

---

## 漏洞反馈机制

如果你发现了安全漏洞或潜在风险，请按以下方式报告：

1. **不要通过公开 Issue 披露漏洞**，以避免被恶意利用。
2. 请发送邮件至项目维护者，主题注明 `[TRIP Security]`。
   - 当前维护者邮箱：zzhou602@seu.edu.cn
3. 报告中请尽量包含：
   - 漏洞类型与影响范围
   - 复现步骤或最小示例
   - 可能的影响与利用条件
   - 建议的修复方案（如有）
4. 维护者将在收到报告后的 5 个工作日内确认，并在修复后公开致谢（如你希望）。

---

## 文件权限参考表

| 路径 | 所有者 | 组 | 建议权限 | 备注 |
| --- | --- | --- | --- | --- |
| `.streamlit/secrets.toml` | 应用运行用户 | 应用运行组 | `600` | 最高敏感度 |
| `runs/` | 应用运行用户 | 应用运行组 | `700` | 含运行历史 |
| `output/` | 应用运行用户 | 应用运行组 | `700` | 输出文件 |
| `.venv/` | 应用运行用户 | 应用运行组 | `755` | 虚拟环境 |
| `trip_ai/`、`skills/`、`app.py` | 应用运行用户 | 应用运行组 | `644` | 只读源码 |
| `LICENSE`、`*.md` | 应用运行用户 | 应用运行组 | `644` | 文档 |

---

## 修订记录

- 2026-07-21：初稿，涵盖密钥管理、外部地址、文件权限与漏洞反馈机制。
