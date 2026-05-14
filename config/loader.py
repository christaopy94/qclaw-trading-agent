#!/usr/bin/env python3
"""
QClaw FinAgent — Configuration Loader
Loads and validates configuration from YAML and environment variables.
"""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from loguru import logger


def load_config() -> dict:
    """
    Load configuration from config/settings.yaml and config/.env.

    Returns:
        dict: Merged configuration dictionary
    """
    # Load environment variables
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        logger.info("Environment variables loaded from config/.env")
    else:
        logger.warning("config/.env not found, using system environment")

    # Load YAML config
    yaml_path = Path(__file__).parent / "settings.yaml"
    if not yaml_path.exists():
        logger.error(f"Config file not found: {yaml_path}")
        return _default_config()

    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Expand environment variable references
    config = _expand_env_vars(config)

    # Merge environment variables (DINGTALK_WEBHOOK_URL etc. at top level)
    config["LLM_API_KEY"] = os.getenv("LLM_API_KEY", "")
    config["DINGTALK_WEBHOOK_URL"] = os.getenv("DINGTALK_WEBHOOK_URL", "")
    config["WECHAT_WEBHOOK_URL"] = os.getenv("WECHAT_WEBHOOK_URL", "")
    config["SLACK_WEBHOOK_URL"] = os.getenv("SLACK_WEBHOOK_URL", "")

    logger.info(f"Configuration loaded | Agent v{config['system']['version']}")
    return config


def _expand_env_vars(config: dict) -> dict:
    """Expand ${VAR} references in config values."""
    import re

    def _resolve(value):
        if isinstance(value, str):
            pattern = re.compile(r'\$\{(\w+)\}')
            for match in pattern.finditer(value):
                env_val = os.getenv(match.group(1), "")
                value = value[:match.start()] + env_val + value[match.end():]
        elif isinstance(value, dict):
            value = {k: _resolve(v) for k, v in value.items()}
        elif isinstance(value, list):
            value = [_resolve(v) for v in value]
        return value

    return _resolve(config)


def _default_config() -> dict:
    """Return default configuration when file is missing."""
    return {
        "system": {"name": "QClaw FinAgent", "version": "0.1.0"},
        "agents": {
            "data": {"enabled": True},
            "sentiment": {"enabled": True, "llm": {"model": "gpt-4", "temperature": 0.3}},
            "strategy": {"enabled": True, "llm": {"model": "gpt-4", "temperature": 0.4}},
            "review": {"enabled": True, "refinement_passes": 3, "llm": {"model": "gpt-4", "temperature": 0.5}},
            "notify": {"enabled": True, "channels": []},
        },
        "workflow": {"daily_review": {"trigger_time": "15:30"}},
        "output": {"directory": "./output"},
    }