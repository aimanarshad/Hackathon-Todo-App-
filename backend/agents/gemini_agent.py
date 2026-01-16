import os
from typing import List
from langchain_core.agents import AgentFinish
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from mcp.tools import get_all_tools


class GeminiAgent:
    def __init__(self):
        # Get the API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        # Initialize the Google Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )

        # Get all tools
        self.tools = get_all_tools()

        # Create memory saver for conversation history
        self.memory = MemorySaver()

        # Create the agent using create_react_agent
        self.agent_executor = create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.memory
        )

    def chat(self, input_text: str, chat_history: List = None) -> dict:
        """
        Process a chat input and return the response

        Args:
            input_text: The user's input message
            chat_history: List of previous messages for context

        Returns:
            Dictionary containing the response and any tool calls
        """
        if chat_history is None:
            chat_history = []

        try:
            # Prepare the input for the react agent
            # The react agent expects a list of messages
            messages = []

            # Add system message if needed
            system_message = {"role": "system", "content": """You are a helpful AI assistant that manages todo tasks.
             Users can ask you to add, list, complete, delete, or update tasks using natural language.
             Use the appropriate tools to interact with the task management system.
             Always respond in a friendly and helpful manner.
             When performing actions, confirm what you're doing and the result.
             If a user request is unclear, ask clarifying questions."""}

            # Add chat history
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Add the current user input
            messages.append({"role": "user", "content": input_text})

            # Execute the agent with the input
            # Using thread_id to maintain conversation state
            config = {"configurable": {"thread_id": "default_thread"}}
            result = self.agent_executor.invoke({"messages": messages}, config=config)

            # Prepare the response
            # Extract the final response from the agent's output
            final_response = ""
            if isinstance(result, dict) and "messages" in result:
                # Look for the last message which should be the AI's response
                for msg in reversed(result["messages"]):
                    if hasattr(msg, 'content'):
                        final_response = msg.content
                        break
                    elif isinstance(msg, dict) and "content" in msg:
                        final_response = msg["content"]
                        break

            response_data = {
                "response": final_response if final_response else "I'm sorry, I couldn't process that request.",
                "tool_calls": []  # Extract tool calls if available
            }

            return response_data

        except Exception as e:
            # Handle any errors gracefully
            return {
                "response": f"I encountered an error: {str(e)}. Please try again.",
                "tool_calls": [],
                "error": str(e)
            }


# Global agent instance
gemini_agent = None


def get_gemini_agent():
    global gemini_agent
    if gemini_agent is None:
        gemini_agent = GeminiAgent()
    return gemini_agent