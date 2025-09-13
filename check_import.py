import os, sys
sys.path.insert(0, os.getcwd())
from src.clients.claude_client import ClaudeClient
c=ClaudeClient(api_key="dummy")
print("Imported ok:",isinstance(c,ClaudeClient))
print("Client object created:", bool(c.client is not None))
