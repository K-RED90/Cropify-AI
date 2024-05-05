from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from .agent_workflow import compile_graph
from models import load_llm
from langchain_core.runnables import Runnable
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import ConfigurableFieldSpec
from pydantic import BaseModel
from typing import Optional, Callable, List
from uuid import uuid4
import tempfile
from langchain_core.messages import HumanMessage, AIMessage
import os
import re
from langchain_core.chat_history import BaseChatMessageHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Create a new database
engine = create_engine("sqlite:///chat_history.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

model = load_llm(model="gpt-3.5-turbo-0125")
graph = compile_graph(llm=model)

router = APIRouter(tags=["chat"])


def _is_valid_identifier(value: str) -> bool:
    """Check if the value is a valid identifier."""
    # Use a regular expression to match the allowed characters
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))


def create_session_factory() -> Callable[[str], BaseChatMessageHistory]:
    """Create a factory that can retrieve chat histories.

    The chat histories are keyed by user ID and conversation ID.

    Args:
        base_dir: Base directory to use for storing the chat histories.

    Returns:
        A factory that can retrieve chat histories keyed by user ID and conversation ID.
    """

    def get_chat_history(user_id: str, conversation_id: str) -> SQLChatMessageHistory:
        """Get a chat history from a user id and conversation id."""
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

    return get_chat_history


class Message(BaseModel):
    messages: List[HumanMessage]


runnable_with_history = RunnableWithMessageHistory(
    runnable=graph,
    get_session_history=create_session_factory(),
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
).with_types(input_type=Message)


@router.post("/chat/", response_model=AIMessage)
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
        return runnable_with_history.invoke(
            {"image_path": None, "messages": request.messages},
            config={
                "configurable": {"user_id": user_id, "conversation_id": conversation_id}
            },
        )
    except Exception as e:
        raise e
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/image")
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

        return output

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def load_db():
    Base.metadata.create_all(engine)
    return session


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