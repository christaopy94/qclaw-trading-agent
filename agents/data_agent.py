#!/usr/bin/env python3
"""
QClaw FinAgent — Data Agent
Collects and structures raw A-share market data for downstream agents.
"""

import asyncio
from datetime import datetime
from typing import Any

import akshare as ak
from loguru import logger
from pydantic import BaseModel


class MarketSnapshot(BaseModel):
    """Structured market data snapshot."""
    date: str
    limit_up_count: int
    limit_down_count: int
    limit_up_stocks: list[dict]
    limit_down_stocks: list[dict]
    board_ladder: dict[str, int]  # {"2B": 12, "3B": 5, ...}
    highest_board: int
    turnover_total: float
    turnover_vs_5d_avg: float
    northbound_flow: float
    timestamp: str


class DataAgent:
    """Agent responsible for collecting market data."""

    def __init__(self, config: dict):
        self.config = config
        self.name = "DataAgent"
        self.enabled = config.get("agents", {}).get("data", {}).get("enabled", True)
        logger.info(f"[{self.name}] Initialized | Enabled: {self.enabled}")

    async def execute(self, target_date: str | None = None) -> MarketSnapshot:
        """
        Execute data collection pipeline.

        Returns:
            MarketSnapshot: Structured market data
        """
        if not self.enabled:
            logger.warning(f"[{self.name}] Agent disabled, skipping execution")
            return None

        date_str = target_date or datetime.now().strftime("%Y-%m-%d")
        logger.info(f"[{self.name}] Starting data collection for {date_str}")

        try:
            # Step 1: Fetch limit-up pool
            limit_up_data = await self._fetch_limit_up_pool(date_str)
            logger.info(f"[{self.name}] Collected {len(limit_up_data)} limit-up stocks")

            # Step 2: Fetch limit-down pool
            limit_down_data = await self._fetch_limit_down_pool(date_str)
            logger.info(f"[{self.name}] Collected {len(limit_down_data)} limit-down stocks")

            # Step 3: Build board ladder
            board_ladder = self._build_board_ladder(limit_up_data)
            highest_board = max([int(k.replace("B", "")) for k in board_ladder.keys()]) if board_ladder else 0
            logger.info(f"[{self.name}] Board ladder: {board_ladder} | Highest: {highest_board}B")

            # Step 4: Fetch market turnover
            turnover_data = await self._fetch_turnover(date_str)

            # Step 5: Fetch northbound flow
            northbound = await self._fetch_northbound_flow(date_str)

            snapshot = MarketSnapshot(
                date=date_str,
                limit_up_count=len(limit_up_data),
                limit_down_count=len(limit_down_data),
                limit_up_stocks=limit_up_data[:50],  # Top 50 for context
                limit_down_stocks=limit_down_data[:20],
                board_ladder=board_ladder,
                highest_board=highest_board,
                turnover_total=turnover_data["total"],
                turnover_vs_5d_avg=turnover_data["vs_5d_avg"],
                northbound_flow=northbound,
                timestamp=datetime.now().isoformat(),
            )

            logger.info(f"[{self.name}] ✅ Data collection complete")
            return snapshot

        except Exception as e:
            logger.exception(f"[{self.name}] Data collection failed: {e}")
            raise

    async def _fetch_limit_up_pool(self, date: str) -> list[dict]:
        """Fetch limit-up (涨停) stocks from AkShare."""
        try:
            # AkShare API: stock_zt_pool_em
            df = ak.stock_zt_pool_em(date=date)
            stocks = []

            for _, row in df.iterrows():
                stock = {
                    "code": row["代码"],
                    "name": row["名称"],
                    "sector": row.get("所属行业", "Unknown"),
                    "limit_up_time": row.get("涨停统计", "Unknown"),  # Simplified
                    "turnover_rate": row.get("换手率", 0.0),
                    "float_mv": row.get("流通市值", 0.0),
                }

                # Filter out excluded boards
                if self._should_exclude(stock):
                    continue

                stocks.append(stock)

            return stocks

        except Exception as e:
            logger.error(f"[{self.name}] Failed to fetch limit-up pool: {e}")
            return []

    async def _fetch_limit_down_pool(self, date: str) -> list[dict]:
        """Fetch limit-down (跌停) stocks."""
        try:
            df = ak.stock_zt_pool_dtgc_em(date=date)
            stocks = []

            for _, row in df.iterrows():
                stock = {
                    "code": row["代码"],
                    "name": row["名称"],
                    "sector": row.get("所属行业", "Unknown"),
                }
                stocks.append(stock)

            return stocks

        except Exception as e:
            logger.error(f"[{self.name}] Failed to fetch limit-down pool: {e}")
            return []

    def _build_board_ladder(self, limit_up_stocks: list[dict]) -> dict[str, int]:
        """
        Build board height ladder from limit-up stocks.

        Returns:
            {"2B": 12, "3B": 5, "4B": 2, "5B": 1}
        """
        ladder = {}
        for stock in limit_up_stocks:
            # Simplified: actual implementation would parse 连板数
            # This is a placeholder
            pass
        return {"2B": 12, "3B": 5, "4B": 2, "5B": 1}

    async def _fetch_turnover(self, date: str) -> dict:
        """Fetch market turnover data."""
        # Placeholder: real implementation would use AkShare
        return {
            "total": 892_000_000_000,  # ¥892B
            "vs_5d_avg": 1.12,  # +12% vs 5-day average
        }

    async def _fetch_northbound_flow(self, date: str) -> float:
        """Fetch northbound fund flow."""
        # Placeholder: real implementation would use AkShare
        return 3_200_000_000  # ¥3.2B net inflow

    def _should_exclude(self, stock: dict) -> bool:
        """Check if stock should be excluded based on config."""
        code = stock.get("code", "")
        name = stock.get("name", "")

        # ChiNext (300xxx), STAR (688xxx), BSE (8xxxxx or 4xxxxx)
        if code.startswith(("300", "688", "8", "4")):
            return True

        # ST stocks
        if "ST" in name or "*ST" in name:
            return True

        return False


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    import json

    async def test():
        agent = DataAgent({"agents": {"data": {"enabled": True}}})
        snapshot = await agent.execute("2026-05-14")
        print(json.dumps(snapshot.model_dump(), indent=2, ensure_ascii=False))

    asyncio.run(test())