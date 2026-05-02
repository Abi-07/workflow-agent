from loguru import logger

logger.add("logs/agent.log", rotation="1 MB")