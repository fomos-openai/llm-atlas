#!/usr/bin/env python3
"""Generate the reviewed v2 knowledge-tree skeleton with substantive article contracts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TODAY = "2026-10-01"

SOURCES = {
    "origins": [
        ("Attention Is All You Need", "https://arxiv.org/abs/1706.03762"),
        ("Language Models are Few-Shot Learners", "https://arxiv.org/abs/2005.14165"),
        ("Training Compute-Optimal Large Language Models", "https://arxiv.org/abs/2203.15556"),
    ],
    "grails": [
        ("Scaling Laws for Neural Language Models", "https://arxiv.org/abs/2001.08361"),
        ("Constitutional AI", "https://arxiv.org/abs/2212.08073"),
        ("Levels of AGI", "https://arxiv.org/abs/2311.02462"),
    ],
    "schools": [
        ("The Llama 3 Herd of Models", "https://arxiv.org/abs/2407.21783"),
        ("DeepSeek-V3 Technical Report", "https://arxiv.org/abs/2412.19437"),
        ("Qwen3 Technical Report", "https://arxiv.org/abs/2505.09388"),
        ("OLMo", "https://arxiv.org/abs/2402.00838"),
    ],
    "lifecycle": [
        ("Training Compute-Optimal Large Language Models", "https://arxiv.org/abs/2203.15556"),
        ("Direct Preference Optimization", "https://arxiv.org/abs/2305.18290"),
        ("FlashAttention", "https://arxiv.org/abs/2205.14135"),
        ("vLLM / PagedAttention", "https://arxiv.org/abs/2309.06180"),
    ],
    "systems": [
        ("Retrieval-Augmented Generation", "https://arxiv.org/abs/2005.11401"),
        ("ReAct", "https://arxiv.org/abs/2210.03629"),
        ("Toolformer", "https://arxiv.org/abs/2302.04761"),
        ("OSWorld", "https://arxiv.org/abs/2404.07972"),
    ],
    "practice": [
        ("LoRA", "https://arxiv.org/abs/2106.09685"),
        ("Direct Preference Optimization", "https://arxiv.org/abs/2305.18290"),
        ("Qwen3 Technical Report", "https://arxiv.org/abs/2505.09388"),
        ("Hugging Face TRL", "https://huggingface.co/docs/trl/index"),
    ],
    "production": [
        ("OWASP Top 10 for LLM Applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
        ("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework"),
        ("vLLM / PagedAttention", "https://arxiv.org/abs/2309.06180"),
    ],
    "state": [
        ("Stanford AI Index", "https://aiindex.stanford.edu/report/"),
        ("The Llama 3 Herd of Models", "https://arxiv.org/abs/2407.21783"),
        ("DeepSeek-V3 Technical Report", "https://arxiv.org/abs/2412.19437"),
        ("Qwen3 Technical Report", "https://arxiv.org/abs/2505.09388"),
    ],
    "future": [
        ("SWE-bench", "https://arxiv.org/abs/2310.06770"),
        ("OSWorld", "https://arxiv.org/abs/2404.07972"),
        ("Constitutional AI", "https://arxiv.org/abs/2212.08073"),
    ],
    "career": [
        ("The Full Stack Deep Learning Course", "https://fullstackdeeplearning.com/"),
        ("Hugging Face LLM Course", "https://huggingface.co/learn/llm-course/"),
        ("PyTorch Documentation", "https://pytorch.org/docs/stable/index.html"),
    ],
    "reference": [
        ("Attention Is All You Need", "https://arxiv.org/abs/1706.03762"),
        ("The Illustrated Transformer", "https://jalammar.github.io/illustrated-transformer/"),
        ("Stanford CRFM", "https://crfm.stanford.edu/"),
    ],
}

PROFILES = {
    "origins": "历史不是模型名称的年表，而是表示学习、可扩展优化、硬件和数据工程共同解除约束的过程。阅读本章时要问：当时真正的瓶颈是什么，新方法改变了哪个约束，又引入了什么新债务。",
    "grails": "圣杯不是营销口号，而是长期目标、可观测代理指标和未解决瓶颈的组合。任何宣称突破的方案都必须说明任务分布、资源预算、失败率和是否存在独立复现。",
    "schools": "所谓技术流派，是一组可复用的架构、训练信号、推理预算与产品假设。比较时必须固定模型规模、数据、延迟和成本，避免用单一榜单把不同优化目标混为一谈。",
    "lifecycle": "Top 模型工程是一条有反馈、有门禁、可回滚的流水线。上游的目标与数据选择会改变下游所有结论；评测、安全和经济性必须在训练前定义，而不是发布前补做。",
    "systems": "系统智能来自模型、上下文、检索、工具、状态、权限和验证器的组合。确定性逻辑应由程序执行，概率性判断交给模型，并为不可逆动作设置显式边界。",
    "practice": "实践以可复现和可解释为第一目标。每次实验固定代码、配置、数据清单和随机种子，先跑 CPU 小样，再进入单卡训练；任何提升都要用独立测试集和成本指标验证。",
    "production": "生产系统关注尾延迟、失败恢复、权限、审计和单位任务成本，而非离线演示。模型只是依赖之一，必须通过网关、策略、观测和降级机制纳入既有工程治理。",
    "state": "现状快照只陈述在核验日期前可追溯的证据。模型自报、第三方复现与真实生产数据分级记录；能力、可靠性、时延和价格分别描述，不发布模糊的‘最强’结论。",
    "future": "未来章节采用情景与证据等级，而非确定性预测。需要区分已经出现的早期信号、尚待规模验证的研究方向，以及依赖重大科学突破的长期假设。",
    "career": "转型目标不是收集术语，而是形成可交付能力：能拆解问题、建立评测、实现训练或系统链路、定位失败并解释成本。学习路线以作品和能力门槛推进。",
    "reference": "参考章节统一术语、公式和诊断入口。它用于快速查证，不替代正文中的因果解释、实现细节和边界条件。",
}

GROUPS: dict[str, list[tuple[str, str, str]]] = {
    "00-navigation": [
        ("README.md", "导航与全景", "用一张全景把生命周期、圣杯、成熟路线、实践和职业五条主线连接起来。"),
        ("complete-lifecycle.md", "完整生命周期", "从问题定义、数据、训练、后训练、评测、发布、运行反馈直到更新与退役建立闭环。"),
        ("five-pillars.md", "五条知识主线", "解释五条主线各自解决的问题、交叉点和推荐阅读顺序。"),
        ("learning-routes.md", "角色化学习路线", "为前端、后端、平台、模型和技术负责人提供不同入口与共同能力门槛。"),
        ("prerequisite-map.md", "前置知识地图", "把数学、深度学习、分布式系统、数据工程和产品安全映射到具体章节。"),
        ("evidence-and-freshness.md", "证据与时效规则", "规定稳定知识、时效快照、厂商自报、第三方复现和推演内容的标记方式。"),
    ],
    "01-origins": [
        ("README.md", "从哪里来", "用约束解除而不是产品发布串联大模型技术史。"),
        ("symbolic-statistical-neural.md", "符号、统计与神经方法", "比较手写规则、概率模型与端到端表示学习的假设和边界。"),
        ("representation-seq2seq-attention.md", "表示学习、Seq2Seq 与注意力", "解释分布式表示、编码器解码器和注意力如何解决长距离依赖与对齐。"),
        ("transformer-and-self-supervision.md", "Transformer 与自监督", "从注意力、残差、归一化和自监督目标解释可并行扩展的基础。"),
        ("pretraining-scaling-in-context-learning.md", "预训练、规模化与上下文学习", "连接经验规模定律、计算最优训练和少样本上下文能力。"),
        ("instruction-alignment-and-chat.md", "指令化、对齐与对话模型", "解释 SFT、偏好反馈和安全约束如何把基础模型变为可交互助手。"),
        ("reasoning-agents-and-multimodality.md", "推理、Agent 与多模态", "梳理推理时计算、工具环境和跨模态表示如何把生成器变为行动系统。"),
        ("compute-data-and-open-ecosystem.md", "算力、数据与开放生态", "分析加速器、公开权重、训练框架和社区复现对扩散速度的作用。"),
        ("timeline.md", "关键技术时间线", "以问题、突破、证据和遗留问题四列记录关键节点。"),
    ],
    "02-grails": [
        ("README.md", "学术与产业圣杯", "用目标、代理指标、瓶颈和成熟度描述长期竞争方向。"),
        ("grail-maturity-matrix.md", "圣杯成熟度矩阵", "统一比较每个圣杯的证据等级、技术路线、可测指标与最大未知。"),
        ("academic/generalization-and-reasoning.md", "泛化与可靠推理", "研究模型能否跨分布组合知识、校准不确定性并给出可验证结论。"),
        ("academic/sample-and-data-efficiency.md", "样本与数据效率", "研究如何用更少、更好、更有课程结构的数据获得同等能力。"),
        ("academic/long-term-memory-and-continual-learning.md", "长期记忆与持续学习", "研究不遗忘、可追溯且能在线吸收新知识的模型与系统。"),
        ("academic/recursive-self-improvement.md", "递归自我改进", "区分合成数据闭环、自动研究、工具增强和真正权重级自改进。"),
        ("academic/world-models-and-embodiment.md", "世界模型与具身智能", "研究预测、规划、因果理解和物理交互如何形成闭环。"),
        ("academic/interpretability-alignment-and-control.md", "可解释、对齐与控制", "研究如何理解内部机制、表达规范并控制高能力系统。"),
        ("academic/ai-for-science.md", "AI for Science", "研究模型在可验证科学环境中提出假设、调用工具并产生新知识。"),
        ("industry/intelligence-per-dollar.md", "单位成本智能", "把任务成功率、延迟、吞吐、能源和总拥有成本放进同一优化目标。"),
        ("industry/reliable-autonomous-agents.md", "可靠自治 Agent", "关注长任务成功率、错误恢复、权限和人工接管成本。"),
        ("industry/proprietary-data-flywheel.md", "专有数据飞轮", "讨论真实反馈、数据权利、质量过滤与持续改进形成的壁垒。"),
        ("industry/realtime-multimodal-interface.md", "实时多模态接口", "关注低延迟语音、视觉、文本和行动统一带来的新交互。"),
        ("industry/private-personal-and-edge-ai.md", "私有、个人与边缘智能", "讨论本地推理、隐私、个性化和设备资源约束。"),
        ("industry/ecosystem-and-platform-dominance.md", "生态与平台优势", "分析模型、开发工具、分发渠道和标准接口的网络效应。"),
        ("industry/safety-governance-and-trust.md", "安全、治理与信任", "把合规、可审计性、事件响应和社会许可视为产品能力。"),
    ],
    "03-mature-technology-schools": [
        ("README.md", "成熟技术流派", "按架构、训练、推理和系统假设比较当下可落地路线。"),
        ("comparison-matrix.md", "技术流派比较矩阵", "用能力、数据、训练成本、推理成本、生态和风险进行同口径比较。"),
        ("dense-decoder-generalist.md", "稠密 Decoder 通用模型", "说明其简单稳定、生态成熟以及计算和内存线性增长的代价。"),
        ("sparse-moe.md", "稀疏 MoE", "解释总参数、激活参数、路由、负载均衡和通信复杂度的权衡。"),
        ("reasoning-first-and-test-time-scaling.md", "推理优先与测试时扩展", "分析验证器强化学习、搜索和推理预算如何交换成本与正确率。"),
        ("long-context-rag-and-memory.md", "长上下文、RAG 与记忆", "区分窗口容量、有效利用、外部检索和持久状态的职责。"),
        ("multimodal-native.md", "原生多模态", "比较组合式编码器与统一 token/统一模型路线。"),
        ("agentic-system.md", "Agentic System", "把模型嵌入工具、环境、验证和恢复循环形成系统能力。"),
        ("small-and-edge-models.md", "小模型与边缘模型", "讨论蒸馏、量化、专门化和设备协同带来的成本优势。"),
        ("open-model-full-stack.md", "开放模型全栈", "评估公开权重、数据、代码、日志和许可证的不同开放层级。"),
        ("case-studies/llama-family.md", "Llama 系列案例", "用公开报告拆解稠密模型、数据规模、后训练和安全发布。"),
        ("case-studies/qwen-family.md", "Qwen 系列案例", "分析多语言、稠密与 MoE、思考模式和开放模型实践。"),
        ("case-studies/deepseek-family.md", "DeepSeek 系列案例", "分析 MLA、MoE、低精度训练和可验证推理路线。"),
        ("case-studies/olmo-family.md", "OLMo 系列案例", "分析数据、代码、检查点和训练日志的开放科学价值。"),
        ("case-studies/mistral-family.md", "Mistral 系列案例", "分析小型稠密模型、滑动窗口与 MoE 的工程取舍。"),
    ],
}

LIFECYCLE = {
    "00-goals": [
        ("capability-contract.md", "能力契约", "在训练前定义用户、任务分布、成功、拒答、风险和资源边界。"),
        ("target-evaluation-suite.md", "目标评测套件", "把能力、安全、稳健性、延迟和成本构造成发布门禁。"),
        ("scaling-plan-and-budget.md", "规模计划与预算", "由目标损失、数据供给、训练 FLOPs、集群效率和推理生命周期反推规模。"),
    ],
    "01-data": [
        ("sources-licenses-and-governance.md", "数据来源、许可与治理", "建立来源、用途、权利、保留期和删除请求的可追溯链。"),
        ("acquisition-and-parsing.md", "采集与解析", "处理网页、代码、论文和多媒体采集中的结构、编码与失败恢复。"),
        ("cleaning-deduplication-and-quality.md", "清洗、去重与质量", "比较规则、模型过滤、近似去重和质量评分对能力与多样性的影响。"),
        ("mixtures-sampling-and-curriculum.md", "数据混合、采样与课程", "把能力目标转为数据权重、温度、阶段和反馈调节策略。"),
        ("synthetic-data.md", "合成数据", "区分扩充、蒸馏、难例生成和验证数据，并控制模型坍塌风险。"),
        ("contamination-and-leakage.md", "污染与泄漏", "识别预训练、后训练、检索和评审器对评测数据的直接或间接泄漏。"),
        ("data-infrastructure.md", "数据基础设施", "设计不可变分片、版本、血缘、质量指标和可恢复的数据流水线。"),
    ],
    "02-tokenization": [
        ("bpe-unigram-and-byte-models.md", "BPE、Unigram 与字节模型", "比较压缩率、词表、未知字符、训练成本和推理长度。"),
        ("multilingual-code-and-numbers.md", "多语言、代码与数字", "评估不同字符系统、空白、标识符和数值表示的公平性。"),
        ("tokenizer-evaluation.md", "Tokenizer 评测", "用压缩率、回退率、边界稳定性和任务表现选择词表。"),
    ],
    "03-architecture": [
        ("decoder-only-transformer.md", "Decoder-only Transformer", "从张量形状、残差流和因果目标解释现代语言模型主干。"),
        ("attention-and-kv-cache.md", "注意力与 KV Cache", "连接训练时注意力、推理缓存、带宽和长上下文成本。"),
        ("position-normalization-and-activation.md", "位置、归一化与激活", "比较 RoPE、RMSNorm、SwiGLU 等组件对稳定性与外推的影响。"),
        ("mixture-of-experts.md", "Mixture of Experts", "解释专家路由、容量、负载均衡、专家并行和推理部署。"),
        ("long-context-architecture.md", "长上下文架构", "区分位置外推、稀疏注意力、上下文并行和真实检索能力。"),
        ("multimodal-architecture.md", "多模态架构", "比较适配器、交叉注意力、统一表示和多模态生成头。"),
        ("state-space-and-hybrid-models.md", "状态空间与混合模型", "讨论线性序列建模、选择性状态和注意力混合的边界。"),
    ],
    "04-training-system": [
        ("accelerator-network-and-storage.md", "加速器、网络与存储", "从 HBM、互连、集合通信和检查点带宽理解集群瓶颈。"),
        ("data-tensor-pipeline-context-expert-parallelism.md", "五类并行策略", "组合数据、张量、流水线、上下文和专家并行并计算通信代价。"),
        ("precision-memory-and-optimizer-state.md", "精度、显存与优化器状态", "拆解参数、梯度、激活、主权重和优化器状态的显存账本。"),
        ("kernels-compilers-and-communication.md", "内核、编译器与通信", "分析算子融合、重计算、通信重叠和形状专门化。"),
        ("checkpointing-and-fault-tolerance.md", "检查点与容错", "设计分片检查点、异步落盘、健康检测和确定性恢复。"),
        ("telemetry-and-capacity-planning.md", "训练遥测与容量规划", "用吞吐、MFU、气泡、网络和异常指标定位损失。"),
    ],
    "05-pretraining": [
        ("objectives-and-loss.md", "预训练目标与损失", "解释 next-token 目标、掩码、长度归一化和辅助损失。"),
        ("optimizer-schedule-and-batch.md", "优化器、学习率与批量", "连接 AdamW、warmup、衰减、梯度噪声和全局批量。"),
        ("scaling-pilots.md", "Scaling Pilot", "通过小规模实验拟合数据、参数、计算和质量的关系。"),
        ("stability-and-failure-diagnosis.md", "稳定性与故障诊断", "处理损失尖峰、溢出、坏批次、通信异常和数据漂移。"),
        ("pretraining-runbook.md", "预训练运行手册", "给出启动、观测、暂停、回滚、验收和交接的控制流程。"),
    ],
    "06-midtraining": [
        ("continued-pretraining.md", "持续预训练", "在保持通用能力的同时吸收新领域知识和分布。"),
        ("domain-and-code-adaptation.md", "领域与代码适配", "设计领域数据、代码执行反馈和通用能力回放。"),
        ("long-context-extension.md", "长上下文扩展", "联合调整位置编码、长度课程、内存与评测。"),
        ("capability-shaping.md", "能力塑形", "用数据阶段和目标函数在后训练前建立数学、代码、工具等先验。"),
    ],
    "07-posttraining": [
        ("posttraining-data.md", "后训练数据", "设计指令、偏好、拒答、工具和多轮轨迹的数据体系。"),
        ("supervised-fine-tuning.md", "监督微调", "控制模板、损失掩码、数据比例、过拟合和能力遗忘。"),
        ("preference-and-reward-modeling.md", "偏好与奖励建模", "从成对比较、标注一致性和奖励校准建立行为信号。"),
        ("dpo-and-offline-preference-optimization.md", "DPO 与离线偏好优化", "解释参考策略、偏好间隔、beta 和离线数据偏差。"),
        ("online-reinforcement-learning.md", "在线强化学习", "讨论采样、奖励、优势估计、约束和训练稳定性。"),
        ("rlaif-and-safety-tuning.md", "RLAIF 与安全训练", "利用模型反馈与规则扩展监督，同时防止评审器偏差自我放大。"),
    ],
    "08-reasoning": [
        ("chain-of-thought-and-test-time-compute.md", "思维链与测试时计算", "区分可见推理文本、内部计算、采样数量和推理预算。"),
        ("verifiers-and-process-rewards.md", "验证器与过程奖励", "比较结果验证、步骤验证、形式执行和模型评审。"),
        ("grpo-and-verifiable-rl.md", "GRPO 与可验证强化学习", "分析组内相对优势、奖励稀疏和可验证任务课程。"),
        ("search-planning-and-reflection.md", "搜索、规划与反思", "组合候选生成、树搜索、工具状态和失败恢复。"),
        ("reasoning-distillation.md", "推理蒸馏", "把高预算轨迹压缩到小模型，同时控制错误推理复制。"),
    ],
    "09-evaluation-and-safety": [
        ("evaluation-system-design.md", "评测系统设计", "从能力契约生成离线、在线、回归和发布门禁。"),
        ("benchmarks-and-statistics.md", "基准与统计", "处理样本量、置信区间、方差、显著性和多重比较。"),
        ("human-and-model-judges.md", "人工与模型评审", "校准偏好、位置、长度、风格和同源模型偏差。"),
        ("contamination-and-gaming.md", "污染与刷榜", "检测训练泄漏、模板记忆、提示敏感和指标投机。"),
        ("safety-alignment-and-red-teaming.md", "安全、对齐与红队", "覆盖滥用、越狱、隐私、偏见、失控和事件演练。"),
        ("agent-and-real-world-evaluation.md", "Agent 与真实任务评测", "测量长任务成功、恢复、权限、成本和环境变化。"),
    ],
    "10-model-engineering": [
        ("distillation.md", "蒸馏", "比较 logits、特征、偏好和推理轨迹蒸馏。"),
        ("quantization.md", "量化", "解释权重、激活、KV 缓存精度与校准数据。"),
        ("pruning-and-sparsity.md", "剪枝与稀疏", "区分非结构化、结构化和动态稀疏的真实加速条件。"),
        ("merging-and-adapters.md", "模型合并与 Adapter", "管理多任务 LoRA、权重合并、冲突和回滚。"),
    ],
    "11-inference": [
        ("decoding.md", "解码", "比较贪心、采样、束搜索、约束解码和停止条件。"),
        ("serving-engines.md", "推理引擎", "拆解模型加载、调度、内核、流式输出和分布式执行。"),
        ("continuous-batching-and-paged-kv.md", "连续批处理与分页 KV", "解释动态到达、显存碎片和 KV 生命周期管理。"),
        ("speculative-decoding.md", "推测解码", "通过草稿模型和验证器减少串行解码步。"),
        ("parallel-inference.md", "并行推理", "比较张量、流水线、专家和数据副本在在线服务中的组合。"),
        ("routing-latency-throughput-and-cost.md", "路由、时延、吞吐与成本", "以任务成功一次的总成本决定模型和预算路由。"),
    ],
    "12-release-and-evolution": [
        ("model-cards-and-release-gates.md", "模型卡与发布门禁", "把训练信息、能力、限制和责任转为可审计发布材料。"),
        ("staged-deployment.md", "分阶段部署", "设计离线、影子、灰度、地域和租户级发布。"),
        ("monitoring-and-feedback.md", "监控与反馈", "连接质量、漂移、安全、成本、用户反馈和数据回流。"),
        ("versioning-and-reproducibility.md", "版本与可复现", "统一权重、代码、配置、数据和评测的版本身份。"),
        ("incident-response.md", "事件响应", "定义检测、隔离、降级、取证、沟通和复盘。"),
        ("update-distillation-and-retirement.md", "更新、蒸馏与退役", "判断继续训练、重新训练、蒸馏、路由或退役的经济与风险门槛。"),
    ],
}

for subdir, items in LIFECYCLE.items():
    GROUPS[f"04-top-model-lifecycle/{subdir}"] = items
GROUPS["04-top-model-lifecycle"] = [("README.md", "Top 模型完整生命周期", "从能力契约到退役给出训练顶级大模型的端到端决策链。")]

GROUPS.update({
    "05-intelligence-systems": [
        ("README.md", "从模型到智能系统", "解释权重之外的上下文、知识、工具、状态、权限和验证。"),
        ("prompt-and-context-engineering.md", "提示与上下文工程", "把指令、示例、状态和约束组织成有限上下文预算。"),
        ("retrieval-reranking-and-rag.md", "检索、重排与 RAG", "设计查询、召回、重排、上下文拼装、引用和忠实度评测。"),
        ("knowledge-graphs-and-grounding.md", "知识图谱与事实落地", "在实体关系、文档证据和生成答案之间建立可追溯连接。"),
        ("working-episodic-and-semantic-memory.md", "工作、情景与语义记忆", "按时间尺度、所有权、写入门槛和遗忘策略设计记忆。"),
        ("tool-calling-and-protocols.md", "工具调用与协议", "定义工具 schema、错误语义、幂等、超时、认证和协议互操作。"),
        ("workflows-versus-agents.md", "工作流与 Agent", "根据任务确定性、状态空间和风险选择固定编排或动态规划。"),
        ("planning-reflection-and-verification.md", "规划、反思与验证", "用计划、执行、观察、校验和重规划组成受控循环。"),
        ("multi-agent-systems.md", "多 Agent 系统", "分析角色分工、共享状态、通信开销和错误相关性。"),
        ("coding-and-computer-use.md", "编码与计算机使用", "将仓库、终端、浏览器和 GUI 转为可观测、可回滚的行动空间。"),
        ("realtime-multimodal-systems.md", "实时多模态系统", "协调音视频采集、编解码、流式推理、中断和延迟预算。"),
        ("agent-evaluation-and-observability.md", "Agent 评测与观测", "记录轨迹、工具结果、状态转移、人工接管和单位成功成本。"),
        ("permissions-sandboxing-and-security.md", "权限、沙箱与安全", "以最小权限、能力令牌、隔离执行和审批门控制行动。"),
    ],
    "06-hands-on-practice": [
        ("README.md", "小模型实践主线", "从数据和最小 Transformer 到对齐、自进化、部署与八卡扩展。"),
        ("learning-outcomes.md", "实践学习成果", "定义每个实验应能解释、运行、测量和排障的能力。"),
        ("compute-cost-and-hardware.md", "算力、成本与硬件", "给出 CPU、小样、24GB 单卡和 8 卡配置的时间与显存账本。"),
        ("experiment-discipline.md", "实验纪律", "固定种子、数据、配置、环境、基线和回归门槛。"),
        ("00-environment-and-baseline.md", "实验 00：环境与基线", "安装依赖、运行 CPU 烟雾测试并记录未训练基线。"),
        ("01-build-data-and-tokenizer.md", "实验 01：数据与 Tokenizer", "构造许可清晰的数据样本，训练词表并测量压缩率。"),
        ("02-build-a-transformer-from-scratch.md", "实验 02：从零实现 Transformer", "实现嵌入、RoPE、因果注意力、MLP、残差和语言模型头。"),
        ("03-pretrain-atlas-125m.md", "实验 03：预训练 Atlas-125M", "在单卡运行缩放后的预训练并观察损失、吞吐和生成样本。"),
        ("04-continue-pretraining-qwen3-0.6b.md", "实验 04：持续预训练 Qwen3-0.6B", "用领域数据适配公开基础模型并防止通用能力遗忘。"),
        ("05-sft-and-lora.md", "实验 05：SFT 与 LoRA", "构造聊天模板、损失掩码和高质量指令数据。"),
        ("06-preference-optimization.md", "实验 06：偏好优化", "训练 DPO 配置并比较帮助性、格式和能力退化。"),
        ("07-verifiable-reinforcement-learning.md", "实验 07：可验证强化学习", "在算术和程序任务上用执行器奖励开展小规模策略优化。"),
        ("08-synthetic-data-curriculum.md", "实验 08：合成数据课程", "生成、去重、验证并按难度组织训练样本。"),
        ("09-self-evolution-loop.md", "实验 09：自进化闭环", "运行生成、验证、回放、再训练和独立回归评测循环。"),
        ("10-evaluation-and-regression.md", "实验 10：评测与回归", "建立能力、安全、格式、延迟和成本的版本比较。"),
        ("11-quantization-and-vllm-serving.md", "实验 11：量化与 vLLM 服务", "导出、量化并通过兼容 API 服务模型。"),
        ("12-rag-and-agent-application.md", "实验 12：RAG 与 Agent 应用", "为模型增加检索、工具、权限和轨迹评测。"),
        ("13-scale-from-one-to-eight-gpus.md", "实验 13：从单卡到八卡", "将单卡配置映射到 FSDP、张量并行和集群检查点。"),
        ("results-and-limitations.md", "实验结果与边界", "区分演示成功、统计提升、分布外失败和不可外推结论。"),
    ],
    "07-production-engineering": [
        ("README.md", "生产工程", "面向资深前后端研发构建可观测、可控、可降级的大模型产品。"),
        ("reference-architecture.md", "生产参考架构", "划分客户端、网关、编排、模型、知识、工具、策略和观测平面。"),
        ("frontend-ai-experience.md", "前端 AI 体验", "处理流式输出、中断、可编辑状态、引用、错误和人机协作。"),
        ("backend-orchestration-and-streaming.md", "后端编排与流式协议", "设计 SSE/WebSocket、任务状态、背压、重试和幂等。"),
        ("model-gateway-routing-and-fallback.md", "模型网关、路由与回退", "统一供应商协议并按质量、成本、区域和错误类型路由。"),
        ("control-plane-and-data-plane.md", "控制平面与数据平面", "分离配置、策略、部署与高吞吐请求执行。"),
        ("identity-permissions-and-multitenancy.md", "身份、权限与多租户", "传播用户身份、租户边界、配额和审计上下文。"),
        ("llmops-evalops-and-observability.md", "LLMOps、EvalOps 与观测", "把提示、模型、数据、轨迹、质量和成本纳入版本化运营。"),
        ("caching-cost-and-capacity.md", "缓存、成本与容量", "设计语义缓存、前缀缓存、配额和峰值容量。"),
        ("secure-tool-execution.md", "安全工具执行", "通过沙箱、超时、网络策略、密钥隔离和审批保护工具调用。"),
        ("deployment-and-progressive-delivery.md", "部署与渐进交付", "使用影子、灰度、A/B、自动回滚和兼容检查。"),
        ("incidents-and-recovery.md", "事故与恢复", "覆盖供应商故障、提示注入、数据泄漏、成本失控和模型退化。"),
    ],
    "08-state-of-the-field": [
        ("README.md", "当下处于什么阶段", "将大模型定义为从生成器向推理与行动系统演进中的技术栈。"),
        ("snapshot-methodology.md", "现状快照方法", "规定证据截止日、来源等级、成熟度刻度和更新方式。"),
    ],
    "08-state-of-the-field/2026-10": [
        ("capability-landscape.md", "能力版图", "按语言、代码、数学、知识、感知、工具和长任务描述锯齿边界。"),
        ("architecture-and-training-radar.md", "架构与训练雷达", "追踪稠密、MoE、低精度、数据课程和训练系统的成熟度。"),
        ("posttraining-and-reasoning-radar.md", "后训练与推理雷达", "追踪偏好优化、可验证强化学习、测试时计算和蒸馏。"),
        ("inference-and-cost-radar.md", "推理与成本雷达", "比较缓存、批处理、推测解码、量化、路由和边缘部署。"),
        ("agents-and-software-engineering.md", "Agent 与软件工程", "区分代码补全、仓库任务、计算机使用和长期自治的成熟度。"),
        ("multimodal-and-embodied-systems.md", "多模态与具身系统", "记录实时语音、视觉理解、生成和机器人闭环的证据。"),
        ("open-and-closed-ecosystems.md", "开放与闭源生态", "按权重、代码、数据、日志、许可证和服务能力比较开放程度。"),
        ("safety-regulation-and-incidents.md", "安全、监管与事件", "跟踪能力评测、部署控制、事件公开和监管框架。"),
        ("maturity-scoreboard.md", "成熟度记分板", "将研究演示、可重复实验、受控生产和大规模运营分层。"),
    ],
    "09-future": [
        ("README.md", "未来要去往何处", "用多情景而非单一预测描述大模型下一阶段。"),
        ("scaling-after-current-paradigms.md", "当前范式之后的规模化", "讨论数据、能耗和边际收益约束下的稀疏、模块化和算法进步。"),
        ("synthetic-data-and-self-improvement.md", "合成数据与自我改进", "评估验证型闭环、模型坍塌、教师依赖和开放式自改进。"),
        ("continual-learning-and-memory.md", "持续学习与记忆", "探索模型在不灾难遗忘的情况下更新知识和技能。"),
        ("long-running-autonomous-agents.md", "长时自治 Agent", "研究错误累积、目标漂移、恢复和社会技术边界。"),
        ("world-models-and-embodiment.md", "世界模型与具身", "连接多模态预测、模拟、规划、控制和真实反馈。"),
        ("ai-for-science-and-engineering.md", "科学与工程智能", "关注可执行实验、形式验证和人类专家协作。"),
        ("alignment-control-and-governance.md", "对齐、控制与治理", "探索能力增长下的监督、隔离、审计和制度设计。"),
        ("hardware-energy-and-economics.md", "硬件、能源与经济", "分析算力供给、内存墙、网络、电力和成本结构。"),
        ("scenarios-and-uncertainties.md", "情景与不确定性", "给出渐进增强、系统突破、平台集中和受限发展等情景。"),
    ],
    "10-career": [
        ("README.md", "从资深研发到大模型专家", "把已有工程能力映射到模型、系统、评测和研究能力。"),
        ("competency-matrix.md", "能力矩阵", "用理解、实现、测量、排障和架构五级刻度评估能力。"),
        ("common-foundation.md", "共同基础", "定义所有路线都需要的 Transformer、数据、评测、推理和安全基础。"),
        ("frontend-to-ai-engineer.md", "前端到 AI Engineer", "利用交互、状态和性能经验进入多模态体验与 Agent 前端。"),
        ("backend-to-llm-platform-engineer.md", "后端到 LLM 平台工程师", "利用 API、分布式和可靠性经验进入网关、编排和服务。"),
        ("data-platform-to-training-engineer.md", "数据平台到训练工程师", "利用流水线、血缘和计算平台经验进入数据与分布式训练。"),
        ("model-and-posttraining-expert.md", "模型与后训练专家", "深入架构、优化、SFT、偏好与强化学习。"),
        ("inference-and-systems-expert.md", "推理与系统专家", "深入内核、并行、调度、缓存和单位成本优化。"),
        ("agent-and-application-expert.md", "Agent 与应用专家", "深入上下文、工具、工作流、评测、权限与产品闭环。"),
        ("evaluation-safety-and-alignment-expert.md", "评测、安全与对齐专家", "建立指标、红队、控制、治理和事件能力。"),
        ("30-day-fast-track.md", "30 天快速路线", "用一个可部署作品建立全链路认知和术语最小集。"),
        ("12-week-core-path.md", "12 周核心路线", "完成从模型机制到训练、评测、RAG、Agent 和服务的主线。"),
        ("6-month-expert-path.md", "6 个月专家路线", "通过专项研究、工业基准和技术写作建立专家深度。"),
        ("portfolio-projects.md", "作品集项目", "定义能证明训练、系统、评测和决策能力的项目证据。"),
        ("interview-and-role-map.md", "岗位与面试地图", "按研究、训练、推理、平台、应用和安全岗位准备。"),
        ("what-not-to-learn-first.md", "不要先学什么", "避免从框架 API、提示技巧、模型新闻和大而全数学开始。"),
    ],
    "11-reference": [
        ("README.md", "参考索引", "提供术语、公式、算法、架构、故障与论文的快速入口。"),
        ("glossary.md", "术语表", "统一中英文概念、缩写、同义词和容易混淆的边界。"),
        ("formulas.md", "核心公式", "汇总注意力、交叉熵、优化、并行、显存和服务指标。"),
        ("algorithm-cards.md", "算法卡片", "用输入、目标、步骤、复杂度和失效模式概括关键算法。"),
        ("architecture-cards.md", "架构卡片", "用组件、数据流、扩展点和风险概括系统模式。"),
        ("failure-mode-index.md", "故障模式索引", "按数据、训练、评测、推理、Agent 和生产分类定位问题。"),
        ("paper-reading-map.md", "论文阅读地图", "按问题和先修关系组织原始论文，而非按热度罗列。"),
        ("faq.md", "常见问题", "回答参数规模、RAG、微调、Agent、算力和职业路线的常见误区。"),
        ("historical-timeline.md", "历史时间线", "提供从统计语言模型到行动系统的紧凑索引。"),
    ],
})


def profile_for(group: str) -> tuple[str, str]:
    if group.startswith("00") or group.startswith("01"):
        return "origins", PROFILES["origins"]
    if group.startswith("02"):
        return "grails", PROFILES["grails"]
    if group.startswith("03"):
        return "schools", PROFILES["schools"]
    if group.startswith("04"):
        return "lifecycle", PROFILES["lifecycle"]
    if group.startswith("05"):
        return "systems", PROFILES["systems"]
    if group.startswith("06"):
        return "practice", PROFILES["practice"]
    if group.startswith("07"):
        return "production", PROFILES["production"]
    if group.startswith("08"):
        return "state", PROFILES["state"]
    if group.startswith("09"):
        return "future", PROFILES["future"]
    if group.startswith("10"):
        return "career", PROFILES["career"]
    return "reference", PROFILES["reference"]


def article(group: str, title: str, thesis: str) -> str:
    key, context = profile_for(group)
    sources = "\n".join(f"- [{name}]({url})" for name, url in SOURCES[key])
    return f"""---
title: "{title}"
pillar: "{group.split('/')[0]}"
audience: "senior-engineer"
last_verified: "{TODAY}"
evidence_level: "E2"
---

# {title}

## 学习目标

本节的核心问题是：{thesis}读完后，应能用自己的语言说明它解决了什么约束，画出主要数据流或训练信号，估算关键资源，并指出至少三种不应使用该方案的场景。

{context}

## 机制与技术骨架

分析 **{title}** 时采用四层模型。第一层是目标：明确优化的是预测损失、任务成功率、偏好、安全边界、延迟还是成本。第二层是信号：说明数据、标签、奖励、检索结果或环境反馈如何进入系统。第三层是状态与计算：列出模型参数、优化器状态、缓存、索引、工具状态及其生命周期。第四层是证据：用隔离的训练集、验证集、回归集和线上指标判断变化是否真实。

工程上先建立最小闭环，再扩大规模。最小闭环必须包含固定输入、可重复配置、基线、失败样本和资源记录。规模化之前要回答：瓶颈在算力、内存、网络、数据质量还是评测分辨率；增加预算能否改变主要误差；失败是否会随长度、并发或工具数量累积。只有这些问题有量化答案，局部优化才有意义。

## 工程决策

1. **定义契约**：记录输入分布、输出格式、成功标准、拒绝条件、资源上限和责任边界。
2. **建立基线**：用最简单、最便宜且可解释的方案测出质量、尾延迟、吞吐和单位成功成本。
3. **分离变量**：一次只改变一个关键因素；数据、模型、提示、采样和评审器必须独立版本化。
4. **保留失败**：失败样本不能只用于“修题”，还要进入分类、根因分析和下一轮独立回归集。
5. **设置回滚**：权重、配置、数据、索引和工具权限都需要稳定身份，任何发布都能恢复到已知状态。

对资深工程师而言，重要的不是记住某个框架参数，而是把方案还原成资源与故障模型。训练阶段关注 token 吞吐、有效批量、数值范围和恢复点；在线阶段关注首 token 延迟、每 token 延迟、队列、缓存命中、外部依赖和人工接管。二者共同决定方案能否进入生产。

## 常见失效模式

- 把离线平均分当作真实用户成功率，忽略任务分布和失败严重度。
- 同时改变数据、模型和评测器，结果无法归因；使用模型评审自身输出而未校准偏差。
- 只汇报最好一次运行，不记录随机种子、方差、异常样本和资源消耗。
- 把“上下文中可见”误认为“模型能够稳定利用”，或把“模型会调用”误认为“工具调用安全”。
- 以更大的模型掩盖数据、接口或权限设计问题，导致成本上升但系统可靠性没有改善。

## 评测与验收

验收采用四组指标：能力指标衡量任务正确率和覆盖；稳健性指标覆盖分布漂移、长输入、对抗输入和依赖故障；系统指标覆盖 P50/P95/P99 延迟、吞吐、显存和恢复时间；责任指标覆盖来源、权限、隐私、审计和人工接管。结果必须同时报告绝对值、相对基线、置信范围、失败样本数量与运行成本。

推荐使用“门禁而非总分”：关键安全或权限用例失败时不得被其他高分抵消；性能提升若导致成本或延迟越界，也不能视为可发布提升。对于时效性内容，所有结论必须带核验日期；对于未来判断，明确标注证据等级和可能推翻判断的观察信号。

## 延伸阅读

{sources}
"""


def main() -> None:
    base = ROOT / "knowledge"
    for group, items in GROUPS.items():
        directory = base / group
        directory.mkdir(parents=True, exist_ok=True)
        for filename, title, thesis in items:
            target = directory / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(article(group, title, thesis), encoding="utf-8")
    print(f"generated {sum(len(items) for items in GROUPS.values())} knowledge articles")


if __name__ == "__main__":
    main()
