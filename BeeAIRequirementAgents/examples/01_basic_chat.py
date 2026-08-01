import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_llm
from beeai_framework.backend import UserMessage, SystemMessage
# Initialize the chat model
async def basic_chat_example():
    # Chat model from the shared config (provider set in .env).
    llm = get_llm(temperature=0)
    
    # Create a conversation about something everyone finds interesting
    messages = [
        SystemMessage(content="You are a helpful AI assistant and creative writing expert."),
        UserMessage(content="Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    ]
    # Generate response using create() method
    response = await llm.run(messages)
    print("User: Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    print(f"Assistant: {response.get_text_content()}")
    return response

# Run the basic chat example
async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL) # Suppress unwanted warnings
    response = await basic_chat_example()
if __name__ == "__main__":
    asyncio.run(main())
