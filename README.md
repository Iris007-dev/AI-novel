# Webnovel Writer (AI-novel fork)

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Upstream](https://img.shields.io/badge/upstream-lingfengQAQ%2Fwebnovel--writer-orange.svg)](https://github.com/lingfengQAQ/webnovel-writer)
[![Based on](https://img.shields.io/badge/version-6.2.1-brightgreen.svg)](.claude-plugin/marketplace.json)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

> **关于本仓库（衍生项目声明）**
>
> 本项目是基于 [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) v6.2.1 的衍生 fork。
> 原始项目采用 GPL v3 协议，本仓库遵循相同协议；原作者版权与署名见 [LICENSE](LICENSE) 与原仓库。
>
> 本 fork 的目标：在保留原始长篇网文创作系统的能力之上，专门服务于**言情长篇（古言 / 现言 / 民国言情 / 幻想言情 / 豪门总裁 / 替身文 / 宫斗宅斗 / 青春甜宠 / 狗血言情 / 种田 / 现言脑洞 / 职场婚恋）**做定制强化。
>
> 关于功能状态与言情增强方向，详见 [§ 言情增强路线图](#言情增强路线图) 与 [§ 给作者：使用方法](#给作者使用方法)。

---

# 原项目简介（上游）

一个跑在 Claude Code 上的长篇网文创作插件。从初始化设定、规划卷纲，到写章、审查、沉淀记忆、查询状态，再到一个只读的可视化面板——整条创作流程都给你串好了。

它想解决的其实就一件事：**让 AI 写到几百章，依然记得住设定、接得住伏笔、守得住大纲。**

一句话定位：这是一套面向长篇连载的一致性系统，不是写完就忘的一次性生成器。

> **v7 重构 RFC 公示中**：上游项目下一代 v7 设计已进入公开意见征集期，详见 [Discussions #118](https://github.com/lingfengQAQ/webnovel-writer/discussions/118)。

## 为什么需要它

长篇创作最难的不是写出第一章，而是写到第 80 章、第 200 章以后仍然保持：

- 角色动机不漂移
- 战力、时间线、地点和世界规则不互相打架
- 伏笔有登记、有推进、有回收
- 爽点、感情线、世界观扩展保持节奏
- 每章写完后事实会沉淀到可检索的状态系统

这套系统做的事，就是把上面这些”必须记住、不能写崩”的约束，变成 Claude Code 会自动执行的步骤：动笔前先查资料，写完后把新发生的事实记下来、做一致性审查，再把最新状态同步进检索索引、章节摘要、长期记忆和 Dashboard。它不只是”会写”，而是边写边攒。

## 核心能力（沿用上游）

| 能力 | 命令 | 说明 |
|------|------|------|
| 深度初始化 | `/webnovel-init` | 分阶段问答，帮你把书的骨架、设定集、总纲和初始状态搭起来 |
| 卷纲规划 | `/webnovel-plan` | 基于总纲拆卷、拆章、补时间线，并写回新增设定 |
| 章节创作 | `/webnovel-write` | 一条龙写完一章：备上下文、起草、审查、润色、记录事实、自动备份 |
| 质量审查 | `/webnovel-review` | 从爽点、一致性、节奏、OOC、连贯性、追读力等维度审查章节 |
| 状态查询 | `/webnovel-query` | 查询角色、伏笔、节奏、实体关系和运行时信息 |
| 项目学习 | `/webnovel-learn` | 把这本书里好用的写法记下来，存进项目长期记忆 |
| 可视化面板 | `/webnovel-dashboard` | 只读浏览项目状态、实体图谱、章节内容和追读力数据 |
| 项目体检 | `/webnovel-doctor` | 阶段感知检查目录、文件、数据库、RAG、依赖和 Dashboard 产物 |

## 给作者：使用方法

### 1. 安装插件

通过 Claude Code Marketplace 安装（在 Claude Code 里运行）：

```bash
# 添加本仓库作为 marketplace
claude plugin marketplace add Iris007-dev/AI-novel --scope user

# 安装（注意：plugin 名按本仓库实际 marketplace.json 调整，下面以原 plugin 名示例）
claude plugin install webnovel-writer@webnovel-writer-marketplace --scope user
```

只想在当前项目生效时，把 `--scope user` 改成 `--scope project`。

> **注意**：本仓库的 `.claude-plugin/marketplace.json` 默认 `owner.name = lingfengQAQ`。
> 改为自有仓库前，建议先把 `marketplace.json` 里的 `owner` / `homepage` 改成自己的信息，
> 这样安装时报错/列表才会显示您自己的仓库作为来源。

### 2. 安装 Python 依赖

```bash
python -m pip install -r requirements.txt
python -m pip install -r webnovel-writer/scripts/requirements.txt
```

### 3. 初始化一本书

在 Claude Code 中输入：

```bash
/webnovel-init
```

初始化完成后会创建书项目目录，包含（详见 `webnovel-writer/commands/webnovel-init.md`）：

```text
project-root/
├── .story-system/        # 合同、章节提交和事件审计
├── .webnovel/            # 状态、索引、摘要、备份和长期记忆
├── 正文/                  # 章节正文
├── 大纲/                  # 总纲、卷纲、时间线和章纲
├── 设定集/                # 世界观、角色、力量体系等设定
└── 审查报告/              # 章节审查报告
```

### 4. 配置 RAG（沿用上游）

进入书项目根目录，把 `.env.example` 复制为 `.env` 并填写 API Key。最小配置：

```bash
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_embed_api_key

RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_rerank_api_key
```

没填 Embedding Key 也能用——系统会自动退回 BM25 关键词检索。

### 5. 开始规划和写作

```bash
/webnovel-plan 1      # 规划第 1 卷
/webnovel-write 1     # 写第 1 章
/webnovel-review 1-5  # 审查第 1-5 章
/webnovel-query 伏笔  # 查询项目状态
```

### 6. 打开可视化面板

```bash
/webnovel-dashboard
```

## 言情增强路线图

下面是本 fork 的**目标强化方向**——针对言情长篇的特性（节奏明快 / 爽点密集 / 情感真实 / 反转精妙 / 高潮迭起 / 代入极强）的实施路线。每项注明预期效果，方便按优先级逐项实施。

> **实施状态**：以下方向尚未合并进当前 commit，作为路线图提供。
> 当前 commit 等价于上游 v6.2.1，**未做任何言情特定改动**。
> 按本路线图实施后，将依次产生 4 轮 commit，每轮都附单元测试。

### 第一轮：长篇一致性基础（防”挖坑忘填”）

**新增**：跨章一致性审查 agent
- 文件：`webnovel-writer/agents/cross-chapter-reviewer.md`
- 作用：专门防长篇最常见的问题——男主第 30 章承诺的事第 80 章忘了；女主第 50 章的人设第 100 章突然漂移
- 检查项（5 类）：未回收伏笔 / 未兑现承诺 / 违反已揭示规则 / 角色承诺漂移 / 时间线跨章跳跃
- 接入点：`webnovel-write` Step 3 后自动调用，非 `--minimal` 模式必须跑

**集成到写章**：
- `skills/webnovel-write/SKILL.md`：新增 Step 1.5（言情题材判定）+ Step 3.5（跨章审查）
- 硬规则加 1 条：禁止跳过跨章审查
- 预期效果：写 200 章不再”前后矛盾”——这是言情读者最大的弃书原因

### 第二轮：言情专属方法论（糖点 / 反转 / 人设）

**新增 4 份言情文档**：
- `references/genres/yanqing-playbook.md`（约 350 行）
  - 6 种言情专属爽点模式（暗涌式心动 / 反差式沦陷 / 误会式心疼 / 公费式撒糖 / 身份式碾压 / 深情式回响）
  - 6 种言情专属反转套路（真假千金 / 重生前世今生 / 失忆认错人 / 复仇反派翻车 / 错位告白 / 破镜重圆）
  - 4 类糖点（微触 / 微甜 / 微酸 / 微烫）+ 10 种微烫糖点模板
  - 9 段情感真实度协议（不直白 / 不悬浮 / 不工具人 / 不完美主义 / 不滥用巧合 / 不悬空台词 / 不靠巧合恋爱 / 不忽视反派动机 / 不滥用巧合反转）
- `references/genres/yanqing-characters.md`（约 320 行）
  - 男主 6 型（高冷霸总 / 温柔守护 / 痞气幽默 / 病娇偏执 / 权谋深沉 / 暗涌隐忍）
  - 女主 6 型（坚韧独立 / 聪慧冷静 / 白月光 / 反差魅力 / 救赎 / 双强）
  - 36 组合矩阵 + 推荐 Top 5 + 高风险组合警告
  - 6 阶段关系糖点映射
- `references/genres/yanqing-chapter-templates.md`（约 480 行）
  - 10 种章节模板（相遇 / 重逢 / 误会 / 心动 / 表白 / 信任危机 / 复仇 / 反派翻车 / 真相大白 / 大婚）
  - 每章含：结构骨架（百分比节奏）+ 糖点位置 + 章末钩子模板句 + 踩坑警示
- `references/genres/yanqing-writer-rules.md`（约 340 行）
  - 6 段硬指标：字数下限 / 节奏变化 / 段落长度 / 对话占比 35-45% / 糖点下限 / 章末钩子必须情感性
  - 反派 5 章必现

**集成**：
- `webnovel-init` Step 3.5 言情人设组合推荐 + Step 3.6 言情细分流派（共 39 个 sub_genre）
- `webnovel-write` Step 1.5 自动加载全部 4 份言情文档

**预期效果**：写出的言情章节糖点密度符合言情读者预期，反派有人话，男女主不人设漂移。

### 第三轮：写章硬指标 + 流派模板扩展

**写章硬指标**：
- 通过 `references/genres/yanqing-writer-rules.md` 把”节奏明快”从形容词变成可量化指标
- 字数下限、对话占比、糖点下限、章末钩子类型——每条都可在 review-pipeline 自动检查

**扩展题材模板**：
- 已扩展：现言脑洞 / 豪门总裁 / 替身文 / 青春甜宠 / 古言 / 宫斗宅斗 / 幻想言情 / 民国言情 / 狗血言情 / 种田 / 职场婚恋（共 11 份言情类模板）
- 每份加 §9 言情套件（流派专属糖点 + 反派配置 + 糖点密度 + Strand 配比）

**跨章审查 issue category**：
- 在 `cross-chapter-reviewer` 加 4 个言情专属 category：`yanqing_monogamy_drift` / `yanqing_character_drift` / `yanqing_sugar_density_low` / `yanqing_villain_absence`
- severity 自动分级，5 章连续 → medium，10 章连续 → high

**预期效果**：每个流派都有专属糖点和反派配置；AI 不再写”全言情用同一套路”。

### 第四轮：CSV / Deconstruction / Quality Trend

**CSV 知识库扩展**（用现有 schema 加 15 条）：
- `桥段套路.csv`：TR-201 破镜重圆 / TR-202 失忆再相恋 / TR-203 带球跑 / TR-204 契约情缘 / TR-205 替身白月光
- `爽点与节奏.csv`：PA-201 公费撒糖 / PA-202 反向告白 / PA-203 暗中守护 / PA-204 心动瞬间 / PA-205 吃醋
- `人设与关系.csv`：CH-201 温柔守护男 / CH-202 病娇偏执男 / CH-203 绿茶女二 / CH-204 救赎女主 / CH-205 双强女主

**拆书专用**：
- `references/genres/yanqing-deconstruction-hints.md`：deconstruction-agent 在题材为言情时自动加载，识别伏笔密度 / 糖点频率 / 言情人设组合 / 反转套路

**Quality Trend**：
- `scripts/quality_trend_report.py` 加 `build_yanqing_quality_section` 函数
- 自动追加 5 个言情专属 trend 字段：糖点密度趋势 / 心动瞬间频率 / 反派活跃度 / 章末钩子类型分布 / 情感一致性

**预期效果**：RAG 检索能命中言情专属条目；拆言情参考书自动识别；Dashboard 能看到言情质量趋势。

### 实施建议

按上面 4 轮顺序逐项合并，每轮独立 commit。每轮完成后跑：
```bash
python -m pytest --no-cov --ignore=test_dashboard_security.py
```

每轮目标新增 20-30 个单元测试，累计 100-150 个言情专属测试。

## 文档导航

| 文档 | 内容 |
|------|------|
| [文档中心](docs/README.md) | 所有文档索引和推荐阅读顺序 |
| [系统架构与模块](docs/architecture/overview.md) | 核心理念、Agent 分工、Story System 设计 |
| [RAG 与配置](docs/guides/rag-and-config.md) | 检索流程、环境变量、默认模型 |
| [题材模板](docs/guides/genres.md) | 37 个题材模板和复合题材规则 |
| [项目结构与运维](docs/operations/operations.md) | 目录层级、健康检查、备份恢复 |
| [插件发版](docs/operations/plugin-release.md) | Marketplace 发版和版本同步流程 |

## 开发与测试

```bash
python -m pip install -r requirements.txt
python -m pip install -r webnovel-writer/scripts/requirements.txt

# 运行测试（注意：test_dashboard_security.py 需要 fastapi）
python -m pytest --ignore=webnovel-writer/scripts/tests/test_dashboard_security.py
```

Dashboard 前端位于 `webnovel-writer/dashboard/frontend/`，发布版已经包含 `dist/` 构建产物。

## 与上游同步

本仓库基于 [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)。
如需把上游更新合并进来：

```bash
git remote add upstream https://github.com/lingfengQAQ/webnovel-writer.git
git fetch upstream
git merge upstream/master   # 或 rebase
```

冲突通常出现在以下位置，请按言情增强方向手动解决：
- `webnovel-writer/agents/cross-chapter-reviewer.md`（本仓库新增）
- `webnovel-writer/references/genres/`（本仓库新增）
- `webnovel-writer/templates/genres/*.md`（追加 §9 言情套件）
- `webnovel-writer/skills/webnovel-write/SKILL.md`（Step 1.5 / 3.5 改动）
- `webnovel-writer/skills/webnovel-init/SKILL.md`（Step 3.5 / 3.6 改动）

## 协议

本仓库采用 **GPL v3** 协议（与上游相同），见 [LICENSE](LICENSE)。

由于 GPL v3 是 copyleft 协议：
- 您可以在本仓库基础上做修改，但发布时必须同样开源
- 必须保留原作者署名（lingfengQAQ）、版权声明、许可证声明
- 修改内容必须明确标注

详细条款见 [LICENSE](LICENSE) 文件或 [GNU 官方网站](https://www.gnu.org/licenses/gpl-3.0.html)。
