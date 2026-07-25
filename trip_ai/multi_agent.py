# Copyright (c) 2025 Southeast University
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

from __future__ import annotations

from dataclasses import dataclass

from .agents.core import GlobalContext, add_metadata
from .agents.dispatch import DISPATCH_SKILL, DispatchAgent
from .agents.event_understanding import EVENT_UNDERSTANDING_SKILL, EventUnderstandingAgent
from .agents.knowledge_retrieval import KNOWLEDGE_RETRIEVAL_SKILL, KnowledgeRetrievalAgent
from .agents.orchestrator import Orchestrator
from .agents.plan_generation import PLAN_GENERATION_SKILL, PlanGenerationAgent
from .agents.risk_assessment import RISK_ASSESSMENT_SKILL, RiskAssessmentAgent


@dataclass(frozen=True)
class MultiAgentApp:
    orchestrator: Orchestrator

    @staticmethod
    def default() -> "MultiAgentApp":
        agents = [
            EventUnderstandingAgent(),
            KnowledgeRetrievalAgent(),
            RiskAssessmentAgent(),
            PlanGenerationAgent(),
            DispatchAgent(),
        ]
        return MultiAgentApp(orchestrator=Orchestrator(agents=agents))

    def run(self, *, ctx: GlobalContext) -> GlobalContext:
        # Allow hot-pluggable skills injected from UI/config.
        skills_override = ctx.working_memory.get("skills_override") or {}
        add_metadata(
            ctx,
            skills_override.get("event-understanding", EVENT_UNDERSTANDING_SKILL),
            skills_override.get("knowledge-retrieval", KNOWLEDGE_RETRIEVAL_SKILL),
            skills_override.get("risk-assessment", RISK_ASSESSMENT_SKILL),
            skills_override.get("plan-generation", PLAN_GENERATION_SKILL),
            skills_override.get("dispatch", DISPATCH_SKILL),
        )
        return self.orchestrator.run(ctx=ctx)
