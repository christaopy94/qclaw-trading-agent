#!/usr/bin/env python3
"""
QClaw FinAgent — Sentiment Agent
Analyzes market sentiment from news, social media, and price behavior.
"""

import asyncio
from datetime import datetime
from enum import Enum
from typing import Any

from loguru import logger
from pydantic import BaseModel


class SentimentLabel(str, Enum):
    EXTREME_GREED = "extreme_greed"
    GREED = "greed"
    NEUTRAL = "neutral"
    FEAR = "fear"
    EXTREME_FEAR = "extreme_fear"


class SentimentScore(BaseModel):
    """Multi-dimensional sentiment scores."""
    news_tone: int  # 0-100
    social_buzz: int  # 0-100
    fear_index: int  # 0-100
    consensus: int  # 0-100
    divergence: int  # 0-100
    overall: int  # 0-100
    label: SentimentLabel
    trend: str  # "rising" | "falling" | "stable"
    timestamp: str


class SentimentReport(BaseModel):
    """Full sentiment analysis report."""
    date: str
    scores: SentimentScore
    market_narrative: str  # What story is the market telling
    key_emotions: list[str]  # e.g., ["optimism", "FOMO", "caution"]
    contrarian_signals: list[str]  # What the market might be missing
    timestamp: str


class SentimentAgent:
    """Agent responsible for sentiment analysis."""

    def __init__(self, config: dict):
        self.config = config
        self.name = "SentimentAgent"
        self.enabled = config.get("agents", {}).get("sentiment", {}).get("enabled", True)
        self.llm_config = config.get("agents", {}).get("sentiment", {}).get("llm", {})
        logger.info(f"[{self.name}] Initialized | Enabled: {self.enabled}")

    async def execute(self, market_snapshot: Any) -> SentimentReport:
        """
        Execute sentiment analysis pipeline.

        Args:
            market_snapshot: Market data from DataAgent

        Returns:
            SentimentReport: Multi-dimensional sentiment analysis
        """
        if not self.enabled:
            logger.warning(f"[{self.name}] Agent disabled, skipping execution")
            return None

        date_str = market_snapshot.date
        logger.info(f"[{self.name}] Starting sentiment analysis for {date_str}")

        try:
            # Step 1: Fetch news sentiment
            news_sentiment = await self._analyze_news_sentiment(date_str)
            logger.info(f"[{self.name}] News tone score: {news_sentiment}")

            # Step 2: Analyze social media buzz
            social_sentiment = await self._analyze_social_buzz(date_str)
            logger.info(f"[{self.name}] Social buzz score: {social_sentiment}")

            # Step 3: Calculate fear index from price behavior
            fear_index = self._calculate_fear_index(market_snapshot)
            logger.info(f"[{self.name}] Fear index: {fear_index}")

            # Step 4: Detect consensus
            consensus = await self._detect_consensus(date_str)
            logger.info(f"[{self.name}] Consensus score: {consensus}")

            # Step 5: Identify divergence signals
            divergence = self._identify_divergence(market_snapshot)
            logger.info(f"[{self.name}] Divergence score: {divergence}")

            # Step 6: Calculate overall score and label
            overall = int((news_sentiment + social_sentiment + (100 - fear_index) + consensus) / 4)
            label = self._score_to_label(overall)
            trend = self._determine_trend(news_sentiment, social_sentiment)

            scores = SentimentScore(
                news_tone=news_sentiment,
                social_buzz=social_sentiment,
                fear_index=fear_index,
                consensus=consensus,
                divergence=divergence,
                overall=overall,
                label=label,
                trend=trend,
                timestamp=datetime.now().isoformat(),
            )

            # Step 7: Generate narrative and signals
            narrative = await self._generate_narrative(market_snapshot, scores)
            key_emotions = await self._identify_key_emotions(scores)
            contrarian_signals = await self._find_contrarian_signals(market_snapshot, scores)

            report = SentimentReport(
                date=date_str,
                scores=scores,
                market_narrative=narrative,
                key_emotions=key_emotions,
                contrarian_signals=contrarian_signals,
                timestamp=datetime.now().isoformat(),
            )

            logger.info(f"[{self.name}] ✅ Sentiment analysis complete | Label: {label.value}")
            return report

        except Exception as e:
            logger.exception(f"[{self.name}] Sentiment analysis failed: {e}")
            raise

    async def _analyze_news_sentiment(self, date: str) -> int:
        """Analyze sentiment from official financial news."""
        # Placeholder: Real implementation would use LLM to analyze news
        # For demo, return simulated score
        return 65

    async def _analyze_social_buzz(self, date: str) -> int:
        """Analyze sentiment from social media and forums."""
        # Placeholder: Real implementation would scrape forums
        return 72

    def _calculate_fear_index(self, snapshot: Any) -> int:
        """Calculate fear index from market behavior."""
        # Higher limit-down count = higher fear
        limit_down_ratio = snapshot.limit_down_count / max(snapshot.limit_up_count, 1)
        fear = min(100, int(limit_down_ratio * 50 + 20))
        return fear

    async def _detect_consensus(self, date: str) -> int:
        """Detect market consensus level."""
        # Placeholder: Real implementation would analyze narrative alignment
        return 58

    def _identify_divergence(self, snapshot: Any) -> int:
        """Identify divergence signals (where bulls and bears disagree)."""
        # High turnover + moderate limit-up = divergence
        if snapshot.turnover_vs_5d_avg > 1.2 and snapshot.limit_up_count < 60:
            return 70
        return 35

    def _score_to_label(self, score: int) -> SentimentLabel:
        """Convert numeric score to sentiment label."""
        if score >= 80:
            return SentimentLabel.EXTREME_GREED
        elif score >= 60:
            return SentimentLabel.GREED
        elif score >= 40:
            return SentimentLabel.NEUTRAL
        elif score >= 20:
            return SentimentLabel.FEAR
        else:
            return SentimentLabel.EXTREME_FEAR

    def _determine_trend(self, news: int, social: int) -> str:
        """Determine sentiment trend."""
        avg = (news + social) / 2
        if avg > 65:
            return "rising"
        elif avg < 45:
            return "falling"
        return "stable"

    async def _generate_narrative(self, snapshot: Any, scores: SentimentScore) -> str:
        """Generate market narrative summary."""
        # Placeholder: Real implementation would use LLM
        return "Market shows cautious optimism with AI sector leading momentum"

    async def _identify_key_emotions(self, scores: SentimentScore) -> list[str]:
        """Identify dominant market emotions."""
        emotions = []
        if scores.social_buzz > 70:
            emotions.append("FOMO")
        if scores.fear_index > 50:
            emotions.append("anxiety")
        if scores.overall > 60:
            emotions.append("optimism")
        return emotions

    async def _find_contrarian_signals(self, snapshot: Any, scores: SentimentScore) -> list[str]:
        """Find contrarian signals (what market might be missing)."""
        signals = []
        if scores.label == SentimentLabel.EXTREME_GREED:
            signals.append("Extreme greed often precedes correction")
        if snapshot.turnover_vs_5d_avg > 1.3:
            signals.append("Unusually high turnover suggests distribution")
        return signals


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    import json

    async def test():
        from agents.data_agent import DataAgent, MarketSnapshot

        config = {"agents": {"sentiment": {"enabled": True}}}
        agent = SentimentAgent(config)

        # Mock snapshot
        snapshot = MarketSnapshot(
            date="2026-05-14",
            limit_up_count=47,
            limit_down_count=8,
            limit_up_stocks=[],
            limit_down_stocks=[],
            board_ladder={"2B": 12, "3B": 5},
            highest_board=5,
            turnover_total=892e9,
            turnover_vs_5d_avg=1.12,
            northbound_flow=3.2e9,
            timestamp="2026-05-14T15:30:00",
        )

        report = await agent.execute(snapshot)
        print(json.dumps(report.model_dump(), indent=2, ensure_ascii=False))

    asyncio.run(test())