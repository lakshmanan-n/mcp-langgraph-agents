class MCPServer:
    def __init__(self):
        self.agents = []

    def register_agent(self, agent):
        self.agents.append(agent)

    def run_interaction(self, message):
        print("MCPServer received message:", message)
        for agent in self.agents:
            message = agent(message)
            print("Processed by agent:", message)
        return message
