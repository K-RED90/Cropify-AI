from fastapi import APIRouter, HTTPException, status, File, UploadFile
from .agent_workflow import compile_graph
from models import load_llm
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import ConfigurableFieldSpec
from pydantic import BaseModel
from typing import Optional, Callable, List, Dict
from uuid import uuid4
import tempfile
from langchain_core.messages import HumanMessage, AIMessage
import os
import re
from langchain_core.chat_history import BaseChatMessageHistory

model = load_llm(model="gpt-3.5-turbo-0125")
graph = compile_graph(llm=model)

router = APIRouter(tags=["chat"])


def _is_valid_identifier(value: str) -> bool:
    """Check if the value is a valid identifier."""
    # Use a regular expression to match the allowed characters
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))


def create_session_factory(user_id: str, conversation_id: str) -> Callable[[str, str], BaseChatMessageHistory]:
    if not _is_valid_identifier(user_id):
        raise ValueError(
            f"User ID {user_id} is not in a valid format. "
            "User ID must only contain alphanumeric characters, "
            "hyphens, and underscores."
            "Please include a valid cookie in the request headers called 'user-id'."
        )
    if not _is_valid_identifier(conversation_id):
        raise ValueError(
            f"Conversation ID {conversation_id} is not in a valid format. "
            "Conversation ID must only contain alphanumeric characters, "
            "hyphens, and underscores. Please provide a valid conversation id "
            "via config. For example, "
            "chain.invoke(.., {'configurable': {'conversation_id': '123'}})"
        )

    id_ = f"{user_id}-{conversation_id}"
    return SQLChatMessageHistory(id_, connection_string="sqlite:///chat_history.db")



class ResponseBody(BaseModel):
    content: str | List[str | Dict]
    additional_kwargs: Dict = {}
    response_metadata: Dict = {}
    type: str = "ai"
    name: str | None = None
    id: str | None  = None
    example: bool = False
    tool_calls: List = []
    invalid_tool_calls: List = []


class Message(BaseModel):
    message: str


runnable_with_history = RunnableWithMessageHistory(
    runnable=graph,
    get_session_history=create_session_factory,
    input_messages_key="messages",
    history_messages_key="chat_history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
).with_types(input_type=[HumanMessage], output_type=AIMessage)


@router.post("/chat/", response_model=ResponseBody)
async def invoke(
    request: Message,
    user_id: Optional[str] = uuid4().hex,
    conversation_id: Optional[str] = uuid4().hex,
) -> dict:
    """
    Handle a chat request and invoke the agent graph with the provided message.

    Args:
        request (Message): The request data containing the chat message and session_id.
        agent (Runnable): The compiled agent graph to invoke.

    Returns:
        dict: The agent's response to the chat message.

    Raises:
        HTTPException: If an exception occurs during the invocation process, a 400 Bad Request error is raised with the exception details.
    """
    try:
        response = runnable_with_history.invoke(
            {"image_path": None, "messages": [HumanMessage(content=request.message)]},
            config={
                "configurable": {"user_id": user_id, "conversation_id": conversation_id}
            },
        )
        return ResponseBody(**response.dict())
    except Exception as e:
        raise e
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/image", response_model=ResponseBody)
async def invoke_with_image(image: UploadFile = File(...)):
    """
    Handle a request with an uploaded image and invoke the agent graph with the image.

    Args:
        image (UploadFile): The uploaded image file.
        agent (Runnable): The compiled agent graph to invoke.

    Returns:
        dict: The agent's response to the image.

    Raises:
        HTTPException: If no image is found in the request or an exception occurs during the invocation process, a 400 Bad Request error is raised with the respective details.
    """
    try:
        if image.file:  # Check if image.file is not None
            with tempfile.NamedTemporaryFile(delete=False) as temp_image:
                contents = image.file.read()  # Read the contents
                temp_image.write(contents)
                image_path = temp_image.name
                print(image_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No image found"
            )

        output = graph.invoke(
            {
                "image_path": image_path,
                "messages": [],
                "chat_history": [],
            }
        )

        if image_path:
            os.remove(image_path)

        return ResponseBody(**output.dict())

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



# Retrieve all conversation history from chat_history.db
@router.get("/history")
async def get_chat_history(user_id: str, conversation_id: str):
    """
    Retrieve all conversation history from chat_history.db.

    Args:
        user_id (str): The user ID.
        conversation_id (str): The conversation ID.
        db (session): The database session.

    Returns:
        list: The conversation history.
    """
    chat_history = SQLChatMessageHistory(
        f"{user_id}-{conversation_id}", connection_string="sqlite:///chat_history.db"
    )
    return await chat_history.aget_messages()


@router.delete("/history")
async def delete_conversation_history(user_id: str, conversation_id: str):
    """
    Delete a conversation history from chat_history.db.

    Args:
        user_id (str): The user ID.
        conversation_id (str): The conversation ID.
        db (session): The database session.

    Returns:
        None
    """
    chat_history = SQLChatMessageHistory(
        f"{user_id}-{conversation_id}", connection_string="sqlite:///chat_history.db"
    )
    await chat_history.aclear()
    return None
