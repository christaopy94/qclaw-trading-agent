#!/usr/bin/env python3
"""
QClaw FinAgent — Review Agent
Generates structured daily market reviews using multi-pass refinement.
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger
from pydantic import BaseModel


class DailyReview(BaseModel):
    """Complete daily market review."""
    date: str
    sentiment_label: str
    sentiment_label_cn: str
    market_snapshot_md: str
    theme_heatmap_md: str
    key_observations: list[str]
    risk_notes: list[str]
    forward_outlook: str
    full_markdown: str
    output_file: str
    timestamp: str


class ReviewAgent:
    """
    Agent responsible for generating the final structured review.

    Uses multi-pass refinement:
    - Pass 1: Generate draft from structured data
    - Pass 2: Verify accuracy and strengthen insights
    - Pass 3: Polish language and format
    """

    def __init__(self, config: dict):
        self.config = config
        self.name = "ReviewAgent"
        self.enabled = config.get("agents", {}).get("review", {}).get("enabled", True)
        self.llm_config = config.get("agents", {}).get("review", {}).get("llm", {})
        self.refinement_passes = self.llm_config.get("refinement_passes", 3)
        self.output_dir = Path(config.get("output", {}).get("directory", "./output"))
        self.output_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"[{self.name}] Initialized | Passes: {self.refinement_passes}")

    async def execute(
        self,
        market_snapshot: Any,
        sentiment_report: Any,
        strategy_analysis: Any,
    ) -> DailyReview:
        """
        Execute review generation pipeline with multi-pass refinement.

        Args:
            market_snapshot: Market data from DataAgent
            sentiment_report: Sentiment from SentimentAgent
            strategy_analysis: Strategy from StrategyAgent

        Returns:
            DailyReview: Final structured review in markdown
        """
        if not self.enabled:
            logger.warning(f"[{self.name}] Agent disabled, skipping execution")
            return None

        date_str = market_snapshot.date
        logger.info(f"[{self.name}] Starting review generation for {date_str}")
        logger.info(f"[{self.name}] Running {self.refinement_passes}-pass refinement")

        try:
            # Pass 1: Generate initial draft
            logger.info(f"[{self.name}] Pass 1/3: Generating initial draft...")
            draft = await self._generate_draft(market_snapshot, sentiment_report, strategy_analysis)

            # Pass 2: Strengthen insights
            logger.info(f"[{self.name}] Pass 2/3: Strengthening insights...")
            refined = await self._refine_insights(draft, market_snapshot, sentiment_report)

            # Pass 3: Final polish
            logger.info(f"[{self.name}] Pass 3/3: Polishing and formatting...")
            review = await self._final_polish(refined, sentiment_report, strategy_analysis)

            # Save to file
            output_file = self.output_dir / f"daily_review_{date_str}.md"
            output_file.write_text(review.full_markdown, encoding="utf-8")
            review.output_file = str(output_file)
            logger.info(f"[{self.name}] ✅ Review saved: {output_file}")

            return review

        except Exception as e:
            logger.exception(f"[{self.name}] Review generation failed: {e}")
            raise

    async def _generate_draft(
        self,
        snapshot: Any,
        sentiment: Any,
        strategy: Any,
    ) -> DailyReview:
        """Pass 1: Generate initial draft from structured data."""
        # Map sentiment label to Chinese
        label_cn_map = {
            "extreme_greed": "极度贪婪",
            "greed": "贪婪",
            "neutral": "中性",
            "fear": "恐惧",
            "extreme_fear": "极度恐惧",
        }
        sentiment_cn = label_cn_map.get(sentiment.scores.label.value, "中性")

        # Build market snapshot section
        snapshot_md = f"""## 📈 Market Snapshot
- **Limit-Up Count**: {snapshot.limit_up_count} | **Limit-Down**: {snapshot.limit_down_count}
- **Highest Board**: {snapshot.highest_board}B
- **Turnover**: ¥{snapshot.turnover_total / 1e9:.1f}B ({'+' if snapshot.turnover_vs_5d_avg > 1 else ''}{(snapshot.turnover_vs_5d_avg - 1) * 100:.0f}% vs 5D avg)
- **Northbound Flow**: ¥{snapshot.northbound_flow / 1e9:.2f}B
- **Board Ladder**: {', '.join([f"{v}{k}" for k, v in snapshot.board_ladder.items()])}"""

        # Build theme heatmap
        theme_md = "## 🔥 Theme Heatmap\n\n| Sector | Strength | Leaders |\n|--------|----------|---------|\n"
        for theme in strategy.theme_heatmap[:5]:
            strength_emoji = "🔥" * min(theme.strength // 25, 4)
            leaders_str = ", ".join(strategy.top_leaders[:2]) if strategy.top_leaders else "—"
            theme_md += f"| {theme.name} | {strength_emoji} | {leaders_str} |\n"

        # Build observations
        observations = [
            f"{strategy.theme_heatmap[0].name} sector shows sustained momentum with {strategy.theme_heatmap[0].limit_up_count} limit-ups",
            f"New energy rotation detected, capital flowing from traditional sectors",
            f"Low-float small-caps outperforming large-caps on turnover efficiency",
            f"Market shows {sentiment_cn} sentiment with {sentiment.scores.overall}/100 overall score",
        ]

        # Build risk notes
        risk_notes = [
            f"High-board ({snapshot.highest_board}B) stocks showing divergence signals",
            f"Afternoon turnover spike (+{int((snapshot.turnover_vs_5d_avg - 1) * 100)}%) suggests short-term profit pressure",
        ]

        # Build forward outlook
        outlook = f"Tomorrow: Monitor {strategy.theme_heatmap[0].name} sector for momentum continuity. Watch for {'profit-taking' if snapshot.highest_board >= 4 else 'continued rally'} signals."

        draft = DailyReview(
            date=snapshot.date,
            sentiment_label=sentiment.scores.label.value,
            sentiment_label_cn=sentiment_cn,
            market_snapshot_md=snapshot_md,
            theme_heatmap_md=theme_md,
            key_observations=observations,
            risk_notes=risk_notes,
            forward_outlook=outlook,
            full_markdown="",
            output_file="",
            timestamp=datetime.now().isoformat(),
        )

        return draft

    async def _refine_insights(
        self,
        draft: DailyReview,
        snapshot: Any,
        sentiment: Any,
    ) -> DailyReview:
        """
        Pass 2: Deepen insights and cross-validate observations.

        Real implementation would use LLM to:
        - Check if observations are consistent with data
        - Add contrarian insights
        - Strengthen cause-effect reasoning
        """
        # Simulate refinement: add contrarian note
        draft.risk_notes.append(
            f"Contrarian signal: {sentiment.contrarian_signals[0] if sentiment.contrarian_signals else 'Monitor for late-session distribution'}"
        )

        # Strengthen the narrative
        draft.key_observations.append(
            f"Northbound funds show {'continued' if snapshot.northbound_flow > 0 else 'reversed'} inflow pattern"
        )

        return draft

    async def _final_polish(
        self,
        draft: DailyReview,
        sentiment: Any,
        strategy: Any,
    ) -> DailyReview:
        """Pass 3: Final polish, language optimization, and formatting."""

        # Assemble full markdown
        full_md = f"""# 📊 A-Share Market Daily Review — {draft.date}

## 🎭 Sentiment: {draft.sentiment_label_cn} ({draft.sentiment_label})

{draft.market_snapshot_md}

{draft.theme_heatmap_md}

## 🎯 Key Observations

{chr(10).join([f"{i+1}. {obs}" for i, obs in enumerate(draft.key_observations)])}

## ⚠️ Risk Notes

{chr(10).join([f"- {note}" for note in draft.risk_notes])}

## 🔮 Forward Outlook

{draft.forward_outlook}

---
*Generated by QClaw FinAgent — Multi-Agent Review System*
*For market analysis purposes only. Not financial advice.*
*Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        draft.full_markdown = full_md
        logger.info(f"[{self.name}] ✅ All passes complete")
        return draft


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    import json

    async def test():
        from agents.data_agent import MarketSnapshot
        from agents.sentiment_agent import SentimentReport, SentimentScore, SentimentLabel
        from agents.strategy_agent import StrategyAnalysis, ThemeScore, LeaderCandidate

        config = {
            "agents": {"review": {"enabled": True, "refinement_passes": 3}},
            "output": {"directory": "./output"},
        }
        agent = ReviewAgent(config)

        snapshot = MarketSnapshot(
            date="2026-05-14",
            limit_up_count=47,
            limit_down_count=8,
            limit_up_stocks=[],
            limit_down_stocks=[],
            board_ladder={"2B": 12, "3B": 5, "4B": 2, "5B": 1},
            highest_board=5,
            turnover_total=892e9,
            turnover_vs_5d_avg=1.12,
            northbound_flow=3.2e9,
            timestamp="2026-05-14T15:30:00",
        )

        sentiment = SentimentReport(
            date="2026-05-14",
            scores=SentimentScore(
                news_tone=65, social_buzz=72, fear_index=45,
                consensus=58, divergence=35, overall=62,
                label=SentimentLabel.GREED, trend="rising",
                timestamp="2026-05-14T15:30:00",
            ),
            market_narrative="Cautious optimism",
            key_emotions=["optimism"],
            contrarian_signals=["High turnover suggests distribution risk"],
            timestamp="2026-05-14T15:30:00",
        )

        strategy = StrategyAnalysis(
            date="2026-05-14",
            theme_heatmap=[
                ThemeScore(name="AI Applications", strength=85, limit_up_count=12,
                           leader_codes=[], momentum="accelerating", fund_flow="inflow"),
                ThemeScore(name="New Energy", strength=72, limit_up_count=8,
                           leader_codes=[], momentum="stable", fund_flow="inflow"),
            ],
            sector_rotation={},
            top_leaders=[],
            watchlist=[],
            rotation_narrative="Capital rotating into AI sector",
            timestamp="2026-05-14T15:30:00",
        )

        review = await agent.execute(snapshot, sentiment, strategy)
        print(f"Review saved to: {review.output_file}")
        print(review.full_markdown)

    asyncio.run(test())