# TRIP Framework Test Report

## 1. Overview

This report covers the inference deployment and test validation of the TRIP (Transport Reasoning with Intelligence Progression) framework on the Orange Pi AI Station powered by Ascend 310P. TRIP is a safety-certification foundation model architecture for complex transportation systems. It bridges the semantic-physical gap by integrating physical constraints with semantic reasoning. This test focuses on **inference-side functionality** and covers the following core features:

- **Multimodal supervised fine-tuning (SFT) model inference:** traffic regulation question answering and scenario decision understanding
- **Reinforcement learning with physical feedback (RLPF) policy model inference:** driving decision generation based on physical rewards
- **Physics-informed tree-of-thought reasoning (PI-ToT):** adaptive physical pruning and safety gating during inference
- **Traffic anomaly detection and decision support:** highway incident detection, semantic parsing, and emergency dispatch recommendation generation
- **MCP automated scenario configuration parsing:** conversion from high-level scenario descriptions to simulation parameters (parsing only, without simulation execution)

**The following items are explicitly excluded from this test scope:** execution of the TASP microscopic simulation engine, because its computational requirements exceed the capacity of the 310P, and model training, including the SFT and RLPF training stages.

The test objective is to verify the functional correctness, inference performance, physical consistency, and deployment feasibility of the TRIP framework on an Ascend 310P edge inference device.

## 2. Version Test Information

**Hardware and version requirements**

- **Product Model:** Orange Pi AI Station
- **AI Processor:** Ascend 310P, with 10 AI Cores, a clock frequency of 1.08 GHz, and 176 TOPS of computing power
- **CPU:** 16 cores, 1.9 GHz
- **Memory:** 48 GB / 96 GB LPDDR4X, 4266 MHz
- **Storage:** NVMe SSD 2280 M.2 slot
- **Operating System:** openEuler 22.03 LTS
- **CANN Version:** CANN 7.0.RC1
- **Driver Version:** 23.0.rc3
- **Python Version:** Python 3.9
- **Inference Framework:** Ollama local model service + MindIE Ascend inference engine

**Test Time:** July 2026

## 3. Test Conclusion

**For the TRIP v1.0 inference release, a total of 98 test cases were executed. Eight issues were identified, including six valid issues: one major issue and five minor issues. The overall quality basically meets the release quality requirements for edge inference deployment. However, inference performance and stability remain subject to the inherent limitations of edge devices, and some high-precision features should be used with caution.**

The framework successfully completed end-to-end **inference-side** deployment on Ascend 310P. The core LLM inference functions, physical consistency validation, and decision generation operated normally. PI-ToT reduced inference latency by 37.5% compared with the baseline, although the absolute latency remained relatively high. Due to the computing and memory limitations of the 310P, the TASP microscopic simulation cannot run locally on the device and must be offloaded to a backend server. Some features requiring high model precision, such as point-cloud modality understanding and precise numerical computation, did not meet expectations and should be degraded or migrated to a platform with greater computing capacity. The Orange Pi device itself has limited stability, does not support continuous 24/7 inference, and provides relatively slow inference speed; user expectations should therefore be set appropriately.

## 4. Feature Quality Assessment

| No. | Feature | Test Conclusion | Functionality | Accuracy | Performance | Reliability | Compatibility |
|------|------|----------|------|------|------|--------|--------|
| 1 | Text-modality SFT model inference (regulation QA and decision understanding) | Passed | Pass | Pass | Pass | Pass | Pass |
| 2 | Image-modality SFT model inference (traffic scenario understanding) | Passed | Pass | Pass | Pass | Pass | Pass |
| 3 | RLPF policy model inference (driving decision generation) | Passed | Pass | Pass | Pass | Pass | Pass |
| 4 | PI-ToT adaptive physical pruning inference | Passed | Pass | Pass | Pass | Pass | Pass |
| 5 | Highway anomaly detection and decision recommendation generation | Passed | Pass | Pass | Pass | Pass | Pass |
| 6 | MCP scenario configuration parsing (DSL → parameters) | Passed | Pass | Pass | Pass | Pass | Pass |
| 7 | Point-cloud modality inference (3D object detection and decision-making) | **Failed** | Pass | **Fail** | Pass | Pass | Pass |
| 8 | Precise numerical computation (flow-delay integration and saturation calculation) | **Failed** | Pass | **Fail** | Pass | Pass | Pass |
| 9 | TASP microscopic simulation engine execution | **Failed** | **Fail** | — | **Fail** | — | — |

**Feature descriptions:**

- **Point-cloud modality inference (failed):** Point-cloud feature extraction accuracy decreased significantly on the 310P, and 3D object localization errors were relatively large, affecting downstream decision reliability. It is recommended to degrade to an image-plus-text multimodal fusion solution or offload processing to a backend server.
- **Precise numerical computation (failed):** FP16 inference caused accumulated floating-point errors. The deviations in engineering calculations such as flow-delay integration and saturation exceeded the acceptable threshold (>5%). It is recommended to transfer critical numerical computations to backend Python scripts and use the LLM only to generate the strategy framework.
- **TASP microscopic simulation (failed):** A microscopic simulation involving 1,000 vehicles requires continuous iteration of vehicle dynamics, car-following models, and signal control. The memory and computing capacity of the 310P cannot support real-time simulation. This feature is a **compute-intensive execution-stage** function and is not a target scenario for the 310P. It has been confirmed that execution must be offloaded to a backend server.

## 5. DFX-Specific Quality Assessment

### 5.1 Security Testing

Overall security test conclusion for the release: **Passed**

- **Security configuration and permission management:** The Ollama inference service runs in a restricted user space, API calls require Token-based authentication, the MindIE inference engine enables security isolation, and the deployment environment enables a firewall with only the necessary ports open: Ollama 11434, Flask 5000, and Socket.IO 8080.
- **Security vulnerability scanning:** CVE scanning was performed on dependencies including Ollama, Flask, transformers, and numpy. No high-risk vulnerabilities were found, and the CANN 7.0 security patches were updated to the latest version.
- **Fuzz testing:** The Ollama RESTful API was subjected to 5,000 random-input fuzz tests, with no crashes or abnormal behavior observed. Adversarial prompt-injection testing was also performed on LLM inputs. The model outputs were filtered by the physical validator, and no non-compliant instructions were generated.
- **Delivery artifact malware scanning:** Model weight files in INT8 and FP16 formats, Docker images, and installation packages all passed ClamAV scanning, and no malicious code was found.

### 5.2 Reliability Testing

| No. | Reliability Feature | Test Conclusion | Residual Risk |
|------|-----------|----------|----------|
| 1 | 24/7 continuous inference stability | **Failed** | The Orange Pi device has limited stability. Long-term operation may occasionally cause system stalling or unexpected service termination. It is recommended to deploy a monitoring daemon that automatically restarts the service after an exception |
| 2 | Continuous inference stability for 8 hours | Passed | None |
| 3 | Graceful degradation when the backend simulator is unavailable | Passed | None |
| 4 | High-concurrency API request handling (≤4 concurrent requests) | Passed | None |
| 5 | Offline inference without network connectivity | Passed | None |
| 6 | Model hot update and rollback | Partially Passed | Hot updates cause a service interruption of 3–5 seconds; low-traffic periods are recommended |

### 5.3 Performance Testing

| Scenario | Model | Feature | Performance Metric | Test Environment | Test Result | Residual Risk |
|------|------|------|----------|----------|----------|----------|
| Inference | DeepSeek-R1-7B (Ollama + MindIE FP16) | PI-ToT single-step inference | Average latency: 1.8 s/step | Orange Pi AI Station 310P | Pass | Inference is relatively slow. A ToT tree with depth >3 has a total latency of approximately 5.4 s and is suitable for offline strategy analysis |
| Inference | DeepSeek-R1-7B (Ollama + MindIE FP16) | Standard ToT baseline | Average latency: 2.9 s/step | Orange Pi AI Station 310P | Pass | PI-ToT reduced latency by 37.5% compared with the baseline, but the absolute latency remained high |
| Inference | SFT base model (Ollama FP16) | Traffic regulation question answering | First-token latency: 850 ms; throughput: 3 QPS | Orange Pi AI Station 310P | Pass | Inference is relatively slow and is suitable for low-frequency decision support |
| Inference | SFT base model (Ollama INT8 quantization) | Traffic regulation question answering | First-token latency: 620 ms; throughput: 5 QPS | Orange Pi AI Station 310P | Pass | The physical consistency metric decreased by approximately 2.3% compared with FP16; FP16 is recommended as the default |
| Multimodal | Joint image-and-text inference (Ollama FP16) | Traffic scenario understanding | End-to-end latency: 2.4 s | Orange Pi AI Station 310P | Pass | Inference is relatively slow |
| Multimodal | Joint point-cloud-and-text inference (Ollama FP16) | 3D scenario understanding | End-to-end latency: 3.2 s; accuracy did not meet the requirement | Orange Pi AI Station 310P | **Fail** | Point-cloud feature extraction accuracy was insufficient; offloading is recommended |
| Numerical computation | Values generated directly by the LLM | Saturation/integration calculation | Result deviation: 6.8% | Orange Pi AI Station 310P | **Fail** | FP16 floating-point errors accumulated; backend computation is recommended |

### 5.4 Compatibility Testing

Compatibility assessment: **Passed**

| No. | Compatibility Scenario | Verification Result | Residual Risk |
|------|-----------|----------|----------|
| 1 | CANN 7.0.RC1 + Ascend 310P | Pass | None |
| 2 | openEuler 22.03 LTS integration | Pass | None |
| 3 | Ollama 0.3.0 + MindIE 1.0 | Pass | None |
| 4 | Ascend 310B backward compatibility verification | Pass | None |
| 5 | Multi-API-provider compatibility (SiliconFlow/Azure) | Pass | None |
| 6 | Frontend React + Socket.IO real-time communication | Pass | None |

## 6. Test Execution Assessment

### 6.1 Test Coverage

| Test Activity | Test Conclusion | Number of Cases | Test Case Coverage | Test Case Pass Rate |
|----------|----------|--------|-----------|-----------|
| Feature testing | Pass | 52 | 100% | 94.2% |
| Performance testing | Pass | 18 | 100% | 88.9% |
| Reliability testing | Pass | 14 | 100% | 85.7% |
| Inherited feature testing | Pass | 8 | 100% | 100% |
| Compatibility testing | Pass | 6 | 100% | 100% |

## 7. Outstanding Issues and Key Risks

| Issue ID | Issue Description | Severity | Impact and Mitigation | Current Status |
|-------|------|-------|---------------|------|
| TRIP-2026-071 | For extremely long text input (>4096 tokens), peak Ascend 310P NPU memory usage approaches the upper limit, occasionally causing OOM | Major | Impact: Parsing of extremely long scenario reports may fail. Mitigation: Enable text segmentation and limit each segment to 2,048 tokens; subsequently optimize KV Cache management | Located, pending fix |
| TRIP-2026-072 | The Orange Pi device is unstable during 24/7 continuous inference, with occasional system stalling and unexpected service termination | Minor | Impact: Unattended long-term operation is not supported. Mitigation: Deploy a systemd daemon for automatic restart; perform a manual inspection every 8 hours; use a backend server as a fallback for critical scenarios | Accepted, inherent device limitation |
| TRIP-2026-073 | Overall inference is relatively slow, with a first-token latency of 850 ms for a single user, 1.8 s for one PI-ToT step, and 2.4 s for multimodal inference | Minor | Impact: Poor experience in high-frequency real-time interaction scenarios. Mitigation: Use streaming output to reduce perceived waiting time; use the lightweight RLPF mode for critical real-time decisions, with a latency of approximately 850 ms; use asynchronous batch processing for complex strategy analysis | Accepted, device computing limitation |
| TRIP-2026-075 | PI-ToT inference is relatively slow, with a single-step latency of 1.8 s and a total latency of 5.4 s when depth >3 | Minor | Impact: Real-time control scenarios are limited. Mitigation: Use direct RLPF decision-making for control scenarios, with a latency of approximately 850 ms, and use PI-ToT only for offline strategy analysis | Accepted, device computing limitation |
| TRIP-2026-076 | During multimodal batch inference, an edge-case warning occurs in the padding alignment between image and text inputs | Minor | Impact: A log warning is generated but result correctness is not affected. Mitigation: Ignore the warning or upgrade the transformers version | Accepted, pending verification |
| TRIP-2026-078 | After INT8 quantization on the 310P, the physical consistency metric decreases by approximately 2.3% | Minor | Impact: The quantized model experiences a slight accuracy loss. Mitigation: Use FP16 inference by default and use INT8 only in extremely resource-constrained scenarios | Accepted, pending optimization |
