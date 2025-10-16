import os
from anthropic import Anthropic
from pydantic import BaseModel
from typing import Type, List, Optional, Literal
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage

from dexter.prompts import DEFAULT_SYSTEM_PROMPT

# Initialize Anthropic client
# Make sure your ANTHROPIC_API_KEY is set in your environment
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Model selection based on task complexity
ModelType = Literal["sonnet", "haiku"]

def get_model_name(model_type: ModelType) -> str:
    """Get the appropriate Claude model based on task complexity."""
    if model_type == "sonnet":
        return "claude-sonnet-4-20250514"  # Sonnet 4.5 for complex analysis
    else:
        return "claude-3-5-haiku-20241022"  # Haiku for fast/bulk tasks

def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    output_schema: Optional[Type[BaseModel]] = None,
    tools: Optional[List[BaseTool]] = None,
    model_type: ModelType = "sonnet",
    temperature: float = 0.0,
) -> AIMessage:
    """
    Call Claude with appropriate model based on task complexity.

    Args:
        prompt: User prompt
        system_prompt: System instructions
        output_schema: Pydantic model for structured output
        tools: List of tools for function calling
        model_type: "sonnet" for complex tasks, "haiku" for fast/bulk
        temperature: Model temperature (0 = deterministic)
    """
    final_system_prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT
    model_name = get_model_name(model_type)

    # Convert langchain tools to Anthropic format if provided
    anthropic_tools = None
    if tools:
        anthropic_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.args_schema.model_json_schema() if hasattr(tool, 'args_schema') else {}
            }
            for tool in tools
        ]

    # Build message
    messages = [{"role": "user", "content": prompt}]

    # Call Anthropic API
    kwargs = {
        "model": model_name,
        "max_tokens": 4096,
        "temperature": temperature,
        "system": final_system_prompt,
        "messages": messages,
    }

    if anthropic_tools:
        kwargs["tools"] = anthropic_tools

    response = anthropic_client.messages.create(**kwargs)

    # Convert to AIMessage format for compatibility
    content = ""
    tool_calls = []

    for block in response.content:
        if block.type == "text":
            content += block.text
        elif block.type == "tool_use":
            tool_calls.append({
                "name": block.name,
                "args": block.input,
                "id": block.id
            })

    ai_message = AIMessage(content=content, tool_calls=tool_calls if tool_calls else None)

    # Handle structured output if requested
    if output_schema:
        import json
        # Parse the content as JSON and validate with Pydantic
        try:
            data = json.loads(content)
            return output_schema(**data)
        except:
            # Fallback: return raw message
            return ai_message

    return ai_message
