from mcp_server.server import MCPServer
from agents.document_ingestor import process_document
from agents.risk_analyzer import analyze_risk

def main():
    server = MCPServer()

    # Register your agents
    server.register_agent(process_document)
    server.register_agent(analyze_risk)

    # Sample input message
    message = {"document_text": "John Doe, DOB 1990-01-01, Address: 123 Main Street"}

    result = server.run_interaction(message)
    print("Final KYC result:", result)

if __name__ == "__main__":
    main()
