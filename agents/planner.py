from config import MAX_AGENT_STEPS
from tools.logger import log_step


class PlanningAgent:

    def __init__(self):

        self.current_step = 0

    def run(self, documents):

        while self.current_step < MAX_AGENT_STEPS:

            self.current_step += 1

            reasoning = "Need to inspect extracted PDF content"

            action = "Analyze document pages"

            result = f"Found {len(documents)} pages"

            log_step(
                self.current_step,
                reasoning,
                action,
                result
            )

            break