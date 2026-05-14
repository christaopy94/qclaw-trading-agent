#!/usr/bin/env python3
"""
QClaw FinAgent — Daily Review Workflow
Orchestrates the complete multi-agent pipeline from data to notification.
"""

import asyncio
import time
from datetime import datetime
from typing import Any

from loguru import logger


class DailyReviewWorkflow:
    """
    Orchestrates the complete daily review pipeline:

    Data Agent → Sentiment Agent → Strategy Agent → Review Agent → Notify Agent

    Each agent receives the output of all previous agents,
    enabling long-chain reasoning across the pipeline.
    """

    def __init__(self, agents: dict, config: dict):
        self.agents = agents
        self.config = config
        self.name = "DailyReviewWorkflow"

    async def execute(self, target_date: str | None = None) -> dict[str, Any]:
        """
        Execute the full multi-agent workflow pipeline.

        Args:
            target_date: Target date string (YYYY-MM-DD). Default: today.

        Returns:
            dict: Execution result with status, output file, and metadata
        """
        start_time = time.time()
        date_str = target_date or datetime.now().strftime("%Y-%m-%d")

        logger.info(f"[{self.name}] ═══════════════════════════════════")
        logger.info(f"[{self.name}] Starting workflow for {date_str}")
        logger.info(f"[{self.name}] ═══════════════════════════════════")

        pipeline_outputs = {}

        try:
            # ─── Step 1: Data Agent ───────────────────────────────────────
            logger.info(f"[{self.name}] Step 1/5: Data Agent — collecting market data")
            t0 = time.time()
            market_snapshot = await self.agents["data"].execute(target_date=date_str)
            pipeline_outputs["market_snapshot"] = market_snapshot
            logger.info(
                f"[{self.name}] ✅ Data collected in {time.time() - t0:.1f}s "
                f"| {market_snapshot.limit_up_count} LU / {market_snapshot.limit_down_count} LD"
            )

            # ─── Step 2: Sentiment Agent ───────────────────────────────────
            logger.info(f"[{self.name}] Step 2/5: Sentiment Agent — analyzing market emotion")
            t0 = time.time()
            sentiment_report = await self.agents["sentiment"].execute(market_snapshot)
            pipeline_outputs["sentiment_report"] = sentiment_report
            logger.info(
                f"[{self.name}] ✅ Sentiment analyzed in {time.time() - t0:.1f}s "
                f"| Label: {sentiment_report.scores.label.value} ({sentiment_report.scores.overall}/100)"
            )

            # ─── Step 3: Strategy Agent ────────────────────────────────────
            logger.info(f"[{self.name}] Step 3/5: Strategy Agent — identifying themes & leaders")
            t0 = time.time()
            strategy_analysis = await self.agents["strategy"].execute(
                market_snapshot=market_snapshot,
                sentiment_report=sentiment_report,
            )
            pipeline_outputs["strategy_analysis"] = strategy_analysis
            logger.info(
                f"[{self.name}] ✅ Strategy analyzed in {time.time() - t0:.1f}s "
                f"| Top theme: {strategy_analysis.theme_heatmap[0].name if strategy_analysis.theme_heatmap else 'N/A'}"
            )

            # ─── Step 4: Review Agent ─────────────────────────────────────
            logger.info(f"[{self.name}] Step 4/5: Review Agent — generating structured review")
            t0 = time.time()
            daily_review = await self.agents["review"].execute(
                market_snapshot=market_snapshot,
                sentiment_report=sentiment_report,
                strategy_analysis=strategy_analysis,
            )
            pipeline_outputs["daily_review"] = daily_review
            logger.info(
                f"[{self.name}] ✅ Review generated in {time.time() - t0:.1f}s "
                f"| Output: {daily_review.output_file}"
            )

            # ─── Step 5: Notify Agent ──────────────────────────────────────
            logger.info(f"[{self.name}] Step 5/5: Notify Agent — delivering notifications")
            t0 = time.time()
            notification_results = await self.agents["notify"].execute(daily_review)
            pipeline_outputs["notification_results"] = notification_results
            notifications_sent = sum(1 for v in notification_results.values() if v)
            logger.info(
                f"[{self.name}] ✅ Notifications sent in {time.time() - t0:.1f}s "
                f"| {notifications_sent}/{len(notification_results)} channels"
            )

            # ─── Finalize ───────────────────────────────────────────────────
            duration = time.time() - start_time

            logger.info(f"[{self.name}] ═══════════════════════════════════")
            logger.info(f"[{self.name}] ✅ Workflow complete | Duration: {duration:.1f}s")
            logger.info(f"[{self.name}] ═══════════════════════════════════")

            return {
                "status": "success",
                "date": date_str,
                "output_file": daily_review.output_file,
                "notifications_sent": notifications_sent,
                "notification_details": notification_results,
                "duration_seconds": duration,
                "pipeline_outputs": pipeline_outputs,
            }

        except Exception as e:
            duration = time.time() - start_time
            logger.exception(f"[{self.name}] ❌ Workflow failed after {duration:.1f}s: {e}")

            return {
                "status": "failed",
                "date": date_str,
                "error": str(e),
                "duration_seconds": duration,
                "pipeline_outputs": pipeline_outputs,
            }


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    from agents import DataAgent, SentimentAgent, StrategyAgent, ReviewAgent, NotifyAgent

    async def test():
        config = {
            "agents": {
                "data": {"enabled": True},
                "sentiment": {"enabled": True},
                "strategy": {"enabled": True},
                "review": {"enabled": True, "refinement_passes": 3},
                "notify": {"enabled": True, "channels": []},
            },
            "output": {"directory": "./output"},
        }

        agents = {
            "data": DataAgent(config),
            "sentiment": SentimentAgent(config),
            "strategy": StrategyAgent(config),
            "review": ReviewAgent(config),
            "notify": NotifyAgent(config),
        }

        workflow = DailyReviewWorkflow(agents, config)
        result = await workflow.execute("2026-05-14")

        print("\n" + "=" * 50)
        print("WORKFLOW RESULT:")
        print("=" * 50)
        import json

        print(json.dumps({k: v for k, v in result.items() if k != "pipeline_outputs"}, indent=2))

        if result["status"] == "success":
            print("\n📝 Review saved:", result["output_file"])

    asyncio.run(test())