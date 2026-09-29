# gino

一组面向行业内容研究的、以证据为中心的 AI Skills。当前仓库覆盖“选题发现与评分”和“获批选题的证据研究”两个相互独立的阶段，并保留一个端到端的市场研究版本。

> 这是给 Claude Code、Codex、OpenClaw 或由 n8n 调度的 AI Agent 使用的技能规范仓库，不是安装后即可自行联网爬取的独立应用。实时搜索、飞书写入和 SEO 数据获取取决于执行环境已经提供并授权的工具。

## 1. 项目解决什么问题

行业博客选题和研究流程常见的问题包括：

- 把新闻标题直接改写成博客选题，缺少买家价值和商业价值判断；
- 热点、常青知识、客户问题和竞争对手内容混在一起，无法稳定分类和排序；
- 同一主题重复生产，或与已有文章产生关键词蚕食；
- 把 Google Trends、PAA、浏览量等代理信号误当成销量或精确搜索量；
- 选题、研究、写作和发布边界不清，导致未经验证的信息进入文章；
- Claude Code、Codex、OpenClaw、n8n 和飞书之间缺少一致的数据契约。

本项目用独立阶段解决这些问题：

```text
Sources -> Signals -> Events / Knowledge Gaps -> Topic Concepts
        -> Deduplication & Scoring -> Human Approval
        -> Evidence Research -> SEO / Writer Handoff
```

`market-topic-v1` 只负责发现、治理和评分选题；获批后再交给 `topic-researcher-v1`。它们都不负责写文章或发布内容。

## 2. 主要功能

### 仓库中的 Skills

| Skill | 用途 | 主要输出 | 明确边界 |
|---|---|---|---|
| [`market-topic-v1`](market-topic-v1/SKILL.md) | 行业热点、常青机会、内容缺口和买家问题的发现、去重、评分与排序 | 符合 Schema 的选题 JSON、四类排行榜、飞书可写入数据 | 停在 Topic Score；不生成 Research Pack、SEO Brief 或文章 |
| [`topic-researcher-v1`](topic-researcher-v1/SKILL.md) | 把已批准的 Topic Card 转换为可追溯的证据研究包 | `research_pack.json`、`research_report.md`、SEO/Writer Handoff | 不发现或重评分选题，不写文章，不制定关键词策略 |
| [`market-research-v3`](market-research-v3/SKILL.md) | 早期端到端方案，将 Topic Scout、Topic Scorer 和 Researcher 放在同一流程 | Topic Database、评分结果、Research Pack | 与上面两个模块化 Skills 有功能重叠，按项目需要二选一 |

### Market Topic V1

- 独立运行 Trend Engine 与 Evergreen Engine；
- 支持 `daily`、`weekly`、`monthly` 三种模式，以及 `focused`、`deep` 两种扫描深度；
- 按七类来源职能规划搜索：官方/一手来源、行业媒体、搜索需求、社区声音、视频创作者、竞争对手、常青知识；
- 将来源规范化为 Signal，将同一真实事件的多篇报道聚类为 Event；
- 用 Industry Knowledge Map 发现常青知识、购买、技术、应用、比较和 FAQ 缺口；
- 先生成 Topic Concept，再生成标题，避免照抄新闻标题；
- 通过 Topic Fingerprint、Overlap Score 和 Topic Intelligence Graph 进行去重、合并、更新与关键词蚕食检查；
- 分别计算 Trend Score、Blog Value Score 和 Final Priority；
- 输出 Breaking/Trending Top 5、Buyer/Commercial Top 5、Evergreen Top 5 和 Overall Top 10；
- 用稳定 ID 保留 `Source -> Signal -> Event / Knowledge Gap -> Topic -> Score` 的完整血缘；
- 可映射到飞书多维表格的 Signals、Events、Topics、Knowledge Map 四张表；
- 提供无第三方 Python 依赖的确定性计分和结果校验脚本。

评分公式：

```text
base_priority = Blog Value Score * 70% + Trend Score * 30%
final_priority = clamp(round(base_priority + boosts + penalties), 0, 100)
```

脚本只复算分数、分档并检查结构和算术；事实判断、来源验证、语义去重和人工批准仍由 Agent 与人工完成。

## 3. 安装方法

### 环境要求

- Git；
- 一个能够读取项目文件并执行任务的 AI Agent，例如 Claude Code、Codex 或 OpenClaw；
- Python 3.9+，仅用于 `market-topic-v1` 的确定性计分和校验脚本；
- 实时选题需要执行环境提供 Web/Search 工具；
- 飞书和 SEO Provider 都是可选项，凭据必须通过运行环境的 Secret 机制提供，不要写入配置、提示词或仓库。

两个 Python 脚本只使用标准库，不需要 `pip install`。

### 克隆仓库

```bash
git clone https://github.com/gino9176/gino.git
cd gino
```

Skills 没有统一的包安装器：

- Claude Code：把仓库放入工作区，并要求它读取目标 Skill 的 `SKILL.md` 和其中指定的 references；
- Codex：将目标 Skill 目录注册到当前 Codex 支持的 Skills 位置后调用，或直接在工作区中指定 `SKILL.md` 路径；
- OpenClaw：把目标 Skill 目录只读挂载给 Agent Job；
- n8n：由 Agent 节点实际执行 Skill，n8n 仅负责定时、传输、重试、存储和通知。

## 4. 使用方法

### 4.1 选择正确的 Skill

- 需要寻找并评分行业选题：使用 `market-topic-v1`；
- 已有获批选题，需要事实和证据研究：使用 `topic-researcher-v1`；
- 需要旧版一体化 Scout → Scorer → Researcher 流程：使用 `market-research-v3`。

不要把 `market-topic-v1` 和 `market-research-v3` 作为同一次任务的两个连续阶段。模块化流程建议使用：

```text
market-topic-v1 -> Human Approval -> topic-researcher-v1
```

### 4.2 创建 Market Topic 配置

```bash
cp market-topic-v1/templates/config.example.yaml market-topic-config.yaml
```

至少填写：

- `industry`
- `product`

建议同时填写目标市场、目标客户、客户角色、语言、运行模式、网站、竞争对手、已有内容和历史 Topic Memory。缺失但不影响核心判断的信息可以由 Agent 保守推断，并必须记录在 `run.assumptions`。

### 4.3 调用 Agent

可对 Claude Code、Codex 或 OpenClaw 使用以下任务说明：

```text
读取 market-topic-v1/SKILL.md，并按其中要求加载 references。
使用 market-topic-config.yaml 执行 weekly / focused 选题扫描。
同时运行 Trend Engine 和 Evergreen Engine。
输出一个符合 market-topic-v1/schemas/output.schema.json 的 result.raw.json。
保留来源、日期、证据类别、假设和覆盖缺口；未知 SEO 指标必须为 null。
在 Topic Score 结束，不要创建 Research Pack、SEO Brief 或文章。
```

如果任务需要当前新闻、法规、SERP 或竞争对手信息，Agent 必须使用实时搜索，不能只依靠模型记忆。

### 4.4 复算分数并校验输出

```bash
python3 market-topic-v1/scripts/calculate_scores.py \
  result.raw.json -o result.json

python3 market-topic-v1/scripts/validate_output.py result.json
```

也可以直接验证仓库自带的完整示例：

```bash
python3 market-topic-v1/scripts/validate_output.py \
  market-topic-v1/templates/result.example.json
```

成功时输出：

```text
PASSED: 0 errors, 0 warning(s)
```

必须修复全部 `ERROR` 后才能交付；`WARNING` 应作为覆盖限制披露。校验脚本不连接网络，也不会替代证据质量判断。

### 4.5 使用 n8n 和飞书

推荐的 n8n 流程：

```text
Schedule Trigger -> Build Config -> Execute Agent -> Parse JSON
-> Validate -> Upsert Feishu -> Notify / Error Branch
```

n8n 不应自行生成选题、修改评分权重、只按标题去重或跳过人工批准。写入飞书前先读取并映射现有表结构，按稳定 ID Upsert，并保留负责人、人工审批、编辑备注、人工优先级和 Researcher 分配等人工字段。

## 5. 输入输出示例

### 输入示例

```yaml
industry: Bicycle manufacturing
product: Aluminum e-bike frames
target_market:
  primary:
    - Netherlands
    - Germany
  secondary:
    - Belgium
    - Poland
target_customer:
  - E-bike brands
  - Bicycle assemblers
customer_roles:
  - Purchasing Manager
  - Product Manager
business_model: B2B
website: https://example.com
competitors: []
languages:
  - en
  - nl
  - de
run_mode: weekly
scan_depth: focused
timezone: Asia/Shanghai
feishu_destination: null
seo_provider: null
existing_content: []
topic_memory: []
knowledge_map: []
extra_constraints:
  - Stop at Topic Score
  - Do not invent SEO metrics
```

输入契约见 [`market-topic-v1/schemas/input.schema.json`](market-topic-v1/schemas/input.schema.json)。`industry` 和 `product` 是必填字段。

### 输出示例

下面是一个 Topic 核心字段节选；完整、可校验的运行结果见 [`market-topic-v1/templates/result.example.json`](market-topic-v1/templates/result.example.json)。

```json
{
  "topic_id": "topic-evaluate-ebike-frame-supplier",
  "topic_concept": "How e-bike brands should evaluate an aluminum frame supplier before RFQ",
  "suggested_title": "How E-Bike Brands Should Evaluate an Aluminum Frame Supplier Before RFQ",
  "topic_type": "EVERGREEN_OPPORTUNITY",
  "content_role": "COMMERCIAL",
  "angle": "BUYING",
  "target_customer": "E-bike brands",
  "primary_role": "Purchasing Manager",
  "buyer_stage": "SELECT",
  "search_intent": "SELECT_SUPPLIER",
  "target_market": ["Netherlands", "Germany"],
  "primary_keyword": "e-bike frame manufacturer",
  "seo_metrics": {
    "search_volume": null,
    "keyword_difficulty": null,
    "cpc": null,
    "provider": null,
    "market": null,
    "measured_at": null
  },
  "scores": {
    "trend": {"total": 20},
    "blog_value": {"total": 88},
    "base_priority": 67.6,
    "final_priority": 73,
    "band": "P2_RECOMMENDED",
    "special_queue": "EVERGREEN_PRIORITY"
  },
  "duplicate_status": "NEW",
  "status": "SCORED"
}
```

完整输出顶层结构为：

```text
run
summary
signals[]
events[]
knowledge_map[]
topics[]
rankings
errors[]
```

输出契约见 [`market-topic-v1/schemas/output.schema.json`](market-topic-v1/schemas/output.schema.json)。

## 项目结构

```text
.
├── README.md
├── market-topic-v1/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   ├── schemas/
│   ├── scripts/
│   └── templates/
├── topic-researcher-v1/
│   ├── SKILL.md
│   ├── references/
│   ├── schemas/
│   ├── examples/
│   └── templates/
└── market-research-v3/
    ├── SKILL.md
    ├── references/
    └── templates/
```

## 重要限制

- 本仓库不包含搜索引擎、爬虫、飞书账号或付费 SEO 数据源；
- 未接入可靠 SEO Provider 时，搜索量、Keyword Difficulty 和 CPC 必须保持 `null`；
- 社区、论坛、评论和视频适合发现问题与语言，不适合单独证明法规、技术限制、市场规模或安全事实；
- `market-topic-v1` 不会自动把选题交给 Researcher，必须先经过人工批准；
- 任一 Skill 都不应绕过付费墙、访问控制、robots 限制或不可用 API；
- 本仓库当前不包含文章写作、编辑、配图或 WordPress 发布 Skill。
