from typing import Any, Dict, List, Optional


class AgentState:
    def __init__(self, user_input: str):
        self.user_input = user_input

        self.intent: Optional[Dict] = None
        self.plan: List[Dict] = []

        self.current_step: int = 0
        self.tool_results: List[Dict] = []

        self.memory: Dict[str, Any] = {}

        self.status: str = "initialized"

        # new fields
        self.retry_count: int = 0
        self.max_retries: int = 2
        self.awaiting_confirmation: bool = False
        self.pending_action: Optional[Dict] = None