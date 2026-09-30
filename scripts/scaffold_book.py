#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from scaffold_v2 import GROUPS, PROFILES


ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = [
    ("01", "一张全景图：从模型到行动系统", ["00-navigation"], "这本书首先建立共同坐标系：大模型不是孤立权重，而是由数据、计算、反馈、检索、工具、权限和运行系统组成的生命周期。"),
    ("02", "从哪里来：七次约束解除", ["01-origins"], "技术史的价值在于解释为什么今天的系统长成这样，以及哪些旧问题只是换了形式再次出现。"),
    ("03", "圣杯：学术目标与产业竞争", ["02-grails"], "圣杯把长期方向变成可观测的工程问题：目标是什么、代理指标是什么、什么证据足以宣布进展。"),
    ("04", "成熟技术流派与公开案例", ["03-mature-technology-schools"], "没有适用于所有任务的单一路线。稠密、MoE、推理优先、检索记忆、多模态、Agent 和小模型各自优化不同约束。"),
    ("05", "目标、数据与 Tokenizer", ["04-top-model-lifecycle/00-goals", "04-top-model-lifecycle/01-data", "04-top-model-lifecycle/02-tokenization"], "训练在第一块 GPU 启动之前就已被目标、评测、数据权利和表示方式决定。"),
    ("06", "架构与训练系统", ["04-top-model-lifecycle/03-architecture", "04-top-model-lifecycle/04-training-system"], "架构决定计算图，训练系统决定它能否以可接受效率和故障率运行。二者必须协同设计。"),
    ("07", "预训练与能力塑形", ["04-top-model-lifecycle/05-pretraining", "04-top-model-lifecycle/06-midtraining"], "预训练学习广泛分布，Mid-training 通过领域、长度和课程塑造后续可对齐能力。"),
    ("08", "后训练、推理与自我改进", ["04-top-model-lifecycle/07-posttraining", "04-top-model-lifecycle/08-reasoning"], "后训练不是润色，它决定模型如何分配推理、遵循偏好、调用工具和表达不确定性。"),
    ("09", "评测、压缩、推理服务与发布", ["04-top-model-lifecycle/09-evaluation-and-safety", "04-top-model-lifecycle/10-model-engineering", "04-top-model-lifecycle/11-inference", "04-top-model-lifecycle/12-release-and-evolution"], "只有被独立评测、成本化、可部署且可回滚的能力，才是工程上可使用的能力。"),
    ("10", "上下文、RAG、记忆与 Agent", ["05-intelligence-systems"], "权重提供先验，系统通过动态知识、工具、状态和权限把先验连接到现实。"),
    ("11", "小模型实践：从零训练到验证闭环", ["06-hands-on-practice"], "实践用两条轨道连接原理和工程：Atlas-125M 解释内部机制，Qwen3-0.6B 演练成熟后训练和服务链路。"),
    ("12", "生产工程与 2026-10 状态", ["07-production-engineering", "08-state-of-the-field"], "生产成熟度由失败恢复、权限、尾延迟、成本和事故能力决定；现状必须按日期和证据等级记录。"),
    ("13", "职业迁移：研发到大模型专家", ["10-career"], "已有工程经验不是包袱。真正需要补足的是模型机制、实验方法、评测和数据—训练—服务之间的闭环。"),
    ("14", "未来：情景、信号与不确定性", ["09-future"], "未来不是一条外推曲线。最有用的判断是明确情景、领先指标、资源约束和能够推翻判断的证据。"),
]

LENSES = {
    "00-navigation": "先画清边界和反馈环，再进入局部技术。一个节点至少要说明输入、输出、所有者、持久状态与失败去向；一条路线至少要说明先修知识和可交付成果。",
    "01-origins": "判断历史突破要看它解除的是表示、优化、并行、数据还是交互约束。新范式通常不会消灭旧问题，只会把瓶颈迁移到新的层级。",
    "02-grails": "圣杯必须拆成能力定义、代理指标、资源预算和反证条件。若一个进展只能在封闭基准或无限预算下成立，它尚未跨越工程门槛。",
    "03-mature-technology-schools": "流派比较要固定任务分布和服务约束。总参数、激活参数、训练 token、推理预算、上下文长度和外部工具都是系统变量，不能只比较模型名称。",
    "04-top-model-lifecycle/00-goals": "能力契约先规定成功与不可接受失败，再倒推评测、数据和预算。没有发布门槛的目标会在训练中不断漂移。",
    "04-top-model-lifecycle/01-data": "数据工程的单位不是文件，而是带来源、许可、转换、质量和用途的样本。任何过滤都会改变分布，任何混合都隐含能力优先级。",
    "04-top-model-lifecycle/02-tokenization": "Tokenizer 同时影响训练长度、语言公平、数字与代码表示以及推理成本。词表选择必须用目标语料的压缩率和下游任务共同评估。",
    "04-top-model-lifecycle/03-architecture": "架构决策最终落到张量形状、访存、通信和可训练性。理论复杂度较低不等于硬件更快，支持长窗口也不等于能可靠使用。",
    "04-top-model-lifecycle/04-training-system": "训练系统要把计算、内存、网络、存储和故障概率组成一张账。扩容前先测量每层时间和通信，否则更多 GPU 可能只放大等待。",
    "04-top-model-lifecycle/05-pretraining": "预训练的核心是稳定地消费正确数据并持续产生可解释损失。损失下降、验证能力、吞吐和数据质量需要同屏观察。",
    "04-top-model-lifecycle/06-midtraining": "Mid-training 用领域、长度和能力课程重新塑造基础模型分布。必须加入通用数据回放并分别测量学习与遗忘。",
    "04-top-model-lifecycle/07-posttraining": "后训练优化的是序列行为而非单纯知识量。模板、标注偏好、拒答和奖励都可能形成捷径，需要独立能力与安全回归。",
    "04-top-model-lifecycle/08-reasoning": "推理能力由策略、预算、搜索空间和验证信号共同决定。更长输出不是充分证据，必须区分正确推理、冗长和奖励投机。",
    "04-top-model-lifecycle/09-evaluation-and-safety": "评测是发布控制面，不是最终宣传表。测试集隔离、方差、失败严重度、评审器校准和线上漂移共同决定可信度。",
    "04-top-model-lifecycle/10-model-engineering": "压缩与适配要比较任务成功一次的总成本。文件更小不代表运行更快，离线误差更低也不保证目标硬件收益。",
    "04-top-model-lifecycle/11-inference": "在线推理是带队列和共享内存的调度系统。首 token、每 token、尾延迟、吞吐、KV 占用和取消行为必须联合测量。",
    "04-top-model-lifecycle/12-release-and-evolution": "发布不是交付终点。版本身份、灰度、监控、反馈权利、事故响应和退役标准共同形成可运营生命周期。",
    "05-intelligence-systems": "系统层通过上下文、知识、工具和状态弥补权重局限，也引入提示注入、权限升级和长任务误差累积。先用固定工作流，再为真正不确定的步骤开放规划。",
    "06-hands-on-practice": "实验先跑最小规模证明正确性，再扩大 token、模型和设备。配置、数据清单、种子、环境和保留集是结果的一部分。",
    "07-production-engineering": "生产链路按控制面与数据面分离，所有外部依赖都要有超时、重试上限、幂等、降级和审计。平均质量不能抵消严重安全失败。",
    "08-state-of-the-field": "现状判断按研究演示、可重复实验、受控生产和大规模稳定运营分层。模型自报与独立证据分开，能力和可靠性分开。",
    "09-future": "未来判断需要领先指标和反证条件。把近中期可验证趋势与依赖科学突破的远期假设分开，避免用情景替代事实。",
    "10-career": "成长以能否独立定义问题、建立基线、实现闭环、定位失败和解释成本为准。作品应留下配置、评测、事故和决策记录。",
    "11-reference": "公式和术语必须连接到实际张量、资源或故障。能查到定义只是起点，能用它解释日志和设计取舍才算掌握。",
}


def matching(prefixes: list[str]):
    for group, items in GROUPS.items():
        if any(group == prefix or group.startswith(prefix + "/") for prefix in prefixes):
            for filename, title, thesis in items:
                if filename == "README.md" and len(items) > 1:
                    continue
                yield group, filename, title, thesis


def page_link(group: str, filename: str) -> str:
    return f"../../knowledge/{group}/{filename}"


def lens_for(group: str) -> str:
    matches = [key for key in LENSES if group == key or group.startswith(key + "/")]
    return LENSES[max(matches, key=len)] if matches else LENSES["11-reference"]


def main() -> None:
    target_dir = ROOT / "book" / "chapters"
    target_dir.mkdir(parents=True, exist_ok=True)
    for number, title, prefixes, opening in CHAPTERS:
        lines = [f"# {number} {title}", "", opening, ""]
        profile_key = "lifecycle" if prefixes[0].startswith("04") else "systems" if prefixes[0].startswith("05") else "practice" if prefixes[0].startswith("06") else "production" if prefixes[0].startswith(("07", "08")) else "future" if prefixes[0].startswith("09") else "career" if prefixes[0].startswith("10") else "origins" if prefixes[0].startswith(("00", "01")) else "grails" if prefixes[0].startswith("02") else "schools"
        lines.extend([PROFILES[profile_key], ""])
        for index, (group, filename, topic, thesis) in enumerate(matching(prefixes), start=1):
            lines.extend([
                f"## {topic}", "",
                thesis + "这要求把概念还原成目标、输入、计算、状态和输出，并明确何种证据能够支持结论。", "",
                lens_for(group), "",
                f"- 决策：在采用“{topic}”前，写出最便宜的基线和它无法满足的硬约束。", 
                f"- 观测：同时记录质量、失败样本、尾延迟、资源与单位成功成本，避免只看单一平均分。",
                f"- 边界：把无法公开验证或尚未实跑的部分标为假设；扩展材料见 [{topic}]({page_link(group, filename)})。", "",
            ])
            if index % 5 == 0:
                lines.extend(["### 阶段复盘", "", "到这里应能画出本阶段的数据流与控制流，列出最可能的三个失败点，并说明下一项投入为什么比扩大模型更优先。", ""])
        path = target_dir / f"{number}-{title.split('：', 1)[0].replace('、', '-').replace(' ', '-').lower()}.md"
        path.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated {len(CHAPTERS)} book chapters")


if __name__ == "__main__":
    main()
