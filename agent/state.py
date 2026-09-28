from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory


class AgentState:
    def __init__(self, user_input: str):
        self.user_input = user_input

        self.intent = None
        self.plan = []

        self.current_step = 0
        self.tool_results = []

        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory()

        self.status = "initialized"

        self.retry_count = 0
        self.max_retries = 2

        self.awaiting_confirmation = False
        self.pending_action = None