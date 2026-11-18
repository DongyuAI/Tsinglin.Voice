# Tsinglin.Voice

语音引擎实测与优化项目的**总览仓**：汇总文档、脚本、版本清单，以及 voxcpm 代码的 subtree 镜像。

## 仓库关系

本项目有两个 GitHub 仓库，代码只维护一份：

| 仓库 | 角色 | 内容 |
|---|---|---|
| `DongyuAI/Tsinglin.Voice`（本仓） | 总览 | 汇总文档、脚本、版本清单；`voxcpm/` 是代码镜像 |
| `DongyuAI/VoxCPM2.cpp` | **代码主仓** | VoxCPM.cpp、audio.cpp、VoxCPM2 工作区的唯一代码副本 |

**代码改动只在 `VoxCPM2.cpp` 仓进行**。本仓的 `voxcpm/` 目录通过 `git subtree` 从主仓同步，不要在两处各改一遍。

## 同步 voxcpm 代码

在**本仓**执行（把主仓 main 的最新代码拉进 `voxcpm/`）：

```bash
git subtree pull --prefix=voxcpm https://github.com/DongyuAI/VoxCPM2.cpp.git main --squash
```

`--squash` 把主仓的多条 commit 压成本仓的一条同步 commit，保持总览仓历史干净。

## 目录结构

```
docs/            汇总报告（实测报告、仓库版本清单、VoxCPM双版本测试报告）
scripts/         辅助脚本（clone、版本采集、缓存路径等）
voxcpm/          ← git subtree, 源: DongyuAI/VoxCPM2.cpp main
  ├── (VoxCPM.cpp 本体: 0.5B 引擎)
  ├── audio.cpp/ (VoxCPM2 引擎 + 优化)
  ├── VoxCPM2/   (工作区: 报告/脚本/探针)
  └── docs/      (跨仓汇总报告)
```

## 环境

- GPU: NVIDIA GTX 1070 8GB（Pascal sm_61）
- CUDA 12.6 + MSVC 19.44（VS2022 BuildTools）
- 编译: 默认 `-j6`，死锁降 `-j3`，严禁 `-j1`
- 缓存: 全部在 `F:\Tsinglin_Voice\.cache`，严禁写 C 盘
- 质量底线: 6 步 / Q8_0 / 不改数值

## 说明

- 第三方 clone 仓库（qwentts.cpp / koboldcpp / CrispASR / whisper.cpp / sherpa-onnx / LLM patch 集合等）**不推源码**，仅在 `docs/仓库版本清单.md` 记录 GitHub 地址与 commit 版本。
- 模型 GGUF、预编译 exe、build 产物不入库。
