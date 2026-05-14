#!/usr/bin/env python3
"""
QClaw FinAgent — Main Entry Point
Multi-Agent Financial Market Analysis & Review Automation System

Usage:
    python main.py --run-once              # Single execution
    python main.py --schedule              # Scheduled daily execution
    python main.py --run-once --date 2026-05-14  # Backfill specific date
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

import typer
from loguru import logger
from rich.console import Console
from rich.panel import Panel

from agents import DataAgent, SentimentAgent, StrategyAgent, ReviewAgent, NotifyAgent
from workflows.daily_review_workflow import DailyReviewWorkflow
from config.loader import load_config

# ─── App Setup ────────────────────────────────────────────────
app = typer.Typer(
    name="QClaw FinAgent",
    help="Multi-Agent Financial Market Analysis System",
    add_completion=False,
)
console = Console()

# ─── Configuration ────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

logger.add(
    OUTPUT_DIR / "agent_runtime.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
)


# ─── Agent Initialization ─────────────────────────────────────
def init_agents(config: dict):
    """Initialize all specialized agents with configuration."""
    logger.info("Initializing agent team...")

    agents = {
        "data": DataAgent(config),
        "sentiment": SentimentAgent(config),
        "strategy": StrategyAgent(config),
        "review": ReviewAgent(config),
        "notify": NotifyAgent(config),
    }

    console.print(
        Panel.fit(
            "\n".join([f"  ✅ {name}: {agent.__class__.__name__}" for name, agent in agents.items()]),
            title="🤖 Agent Team Ready",
            border_style="green",
        )
    )
    return agents


# ─── Run Workflow ─────────────────────────────────────────────
async def run_daily_review(config: dict, target_date: str | None = None):
    """Execute the full daily review workflow."""
    date_str = target_date or datetime.now().strftime("%Y-%m-%d")

    console.rule(f"[bold blue]QClaw FinAgent — Daily Review: {date_str}")

    agents = init_agents(config)
    workflow = DailyReviewWorkflow(agents, config)

    try:
        logger.info(f"Starting daily review workflow for {date_str}")
        result = await workflow.execute(target_date=date_str)

        if result["status"] == "success":
            console.print(
                Panel.fit(
                    f"📝 Review saved: {result['output_file']}\n"
                    f"📨 Notifications sent: {result['notifications_sent']} channels\n"
                    f"⏱️  Total time: {result['duration_seconds']:.1f}s",
                    title="✅ Workflow Complete",
                    border_style="green",
                )
            )
        else:
            console.print(f"[red]❌ Workflow failed: {result['error']}")

    except Exception as e:
        logger.exception(f"Workflow execution failed: {e}")
        console.print(f"[red]❌ Critical error: {e}")
        sys.exit(1)


# ─── Schedule Mode ────────────────────────────────────────────
def run_scheduled(config: dict):
    """Run the agent in scheduled mode (auto-trigger at market close)."""
    from apscheduler.schedulers.asyncio import AsyncIOScheduler

    scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
    trigger_time = config.get("workflow", {}).get("daily_review", {}).get("trigger_time", "15:30")
    hour, minute = map(int, trigger_time.split(":"))

    scheduler.add_job(
        lambda: asyncio.create_task(run_daily_review(config)),
        "cron",
        day_of_week="mon-fri",
        hour=hour,
        minute=minute,
    )

    console.print(
        Panel.fit(
            f"⏰ Scheduled: Mon-Fri at {trigger_time} CST\n"
            "📊 Auto-trigger will execute daily review workflow\n"
            "Press Ctrl+C to stop",
            title="🔄 Scheduled Mode",
            border_style="yellow",
        )
    )

    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user")
        console.print("\n👋 QClaw FinAgent shutting down. Goodbye!")


# ─── CLI Commands ─────────────────────────────────────────────
@app.command()
def run_once(
    date: str = typer.Option(None, help="Target date (YYYY-MM-DD). Default: today"),
):
    """Execute a single daily review workflow."""
    config = load_config()
    asyncio.run(run_daily_review(config, target_date=date))


@app.command()
def schedule():
    """Run in scheduled mode (auto-trigger daily at market close)."""
    config = load_config()
    run_scheduled(config)


@app.command()
def info():
    """Display system information."""
    config = load_config()
    console.print(
        Panel.fit(
            f"  System: {config['system']['name']} v{config['system']['version']}\n"
            f"  LLM Model: {config['agents']['review']['llm']['model']}\n"
            f"  Output Dir: {config['output']['directory']}\n"
            f"  Channels: {', '.join(config['agents']['notify']['channels'])}",
            title="ℹ️ System Information",
        )
    )


# ─── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app()