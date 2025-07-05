# Placeholder agent loop
class AgentLoop:
    def __init__(self, goal):
        self.goal = goal
        self.steps = []

    def run(self):
        print(f"Running agent loop with goal: {self.goal}")
