import json
import os
from memory.schema import MemoryData

MEMORY_FILE = "memory.json"


class LongTermMemory:

    def __init__(self):
        self.memory = self._load()

    def _load(self) -> MemoryData:
        if not os.path.exists(MEMORY_FILE):
            return MemoryData()

        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            return MemoryData(**data)

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory.model_dump(), f, indent=2)

    def get_preferences(self):
        return self.memory.preferences

    def update_preferences(self, updates: dict):
        for key, value in updates.items():
            setattr(self.memory.preferences, key, value)
        self.save()

    def store_event(self, title: str, event_id: str):
        self.memory.last_events[title] = event_id
        self.save()

    def get_event(self, title: str):
        return self.memory.last_events.get(title)