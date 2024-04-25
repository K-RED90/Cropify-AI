from typing import TypedDict, Optional, Type, Callable, Union, Dict
from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, root_validator
from langchain_core.language_models import BaseChatModel
from .core import (
    input_validator,
    search_content_evaluator,
    farm_llm,
    rag_agent,
    fallback_response,
    pest_and_disease_tool,
    encode_image,
    Pest,
    Disease,
    PestOrDisease,
)
from .prompts import (
    PEST_PROMPT,
    DISEASE_PROMPT,
    IMAGE_CLASSIFICATION_PROMPT,
    DEFAULT_MESSAGE,
)
from .tools import search_tool
from langchain_core.runnables import Runnable
from functools import partial


class AgentState(TypedDict):
    input: Optional[str | BaseMessage] = None
    image_path: Optional[str] = None
    chat_history: list[BaseMessage]
    search_results: Optional[str]
    label: Optional[Type[BaseMessage]]
    agent_outcome: Union[AIMessage, Type[BaseModel], Dict]
    images_analysis: Type[BaseModel] | Dict = None


class AgentNodes(BaseModel):
    llm: Optional[BaseChatModel] = None
    vision_tool: Optional[Callable] = None

    @root_validator
    def check_llm(cls, values):
        if values["llm"] is None:
            try:
                from langchain_openai.chat_models import ChatOpenAI
            except ImportError:
                raise ImportError(
                    "Please install the openai plugin to use the default LLM. Run `pip install langchain-openai`"
                )
            values["llm"] = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)

        if values["vision_tool"] is None:
            try:
                from langchain_anthropic.chat_models import ChatAnthropic
            except ImportError:
                raise ImportError(
                    "Please install the anthropic plugin to use the default LLM. Run `pip install langchain-anthropic`"
                )
            vision_model = ChatAnthropic(
                model="claude-3-haiku-20240307", temperature=0.0
            )
            values["vision_tool"] = partial(pest_and_disease_tool, llm=vision_model)
        return values

    def router(self, state: AgentState):
        """Validate the user's input to determine if it is farm-related or not.

        Args:
            state (AgentState): The state of the agent

        Returns:
            str: The output of the validation
        """
        if state["image_path"] is not None:
            image = encode_image(state["image_path"])
            output = self.vision_tool(
                img_base64=image,
                prompt_template=IMAGE_CLASSIFICATION_PROMPT,
                schema=PestOrDisease,
            )
            if output.label == "pest":
                return "pest"
            elif output.label == "disease":
                return "disease"
            else:
                return "other"
        else:
            chain = input_validator(self.llm)
            output = chain.invoke(state)
            return output.is_farm_related

    def crop_disease_node(self, state: AgentState) -> dict[str, AIMessage]:
        """Identify the crop disease from the user's input.

        Args:
            state (AgentState): The state of the agent

        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        image = encode_image(state["image_path"])
        output = self.vision_tool(
            img_base64=image,
            prompt_template=DISEASE_PROMPT,
            schema=Disease,
        )
        return {
            "images_analysis": output,
            "input": str(output.name) + " treatment OR control",
        }

    def crop_pest_node(self, state: AgentState) -> dict[str, AIMessage]:
        """Identify the crop pest from the user's input.

        Args:
            state (AgentState): The state of the agent

        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        image = encode_image(state["image_path"])
        output = self.vision_tool(
            img_base64=image, prompt_template=PEST_PROMPT, schema=Pest
        )
        return {
            "images_analysis": output,
            "input": str(output.name) + " treatment OR control",
        }

    def unrelated_image_node(self, state: AgentState) -> dict[str, AIMessage]:
        """When the image is not related to crop pests or diseases.

        Args:
            state (AgentState): The state of the agent

        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        return {"agent_outcome": AIMessage(content=DEFAULT_MESSAGE)}

    def search_engine_node(self, state: AgentState) -> dict:
        """Search the input query using the search tool.

        Args:
            state (AgentState): The state of the agent

        Returns:
            dict: The search results
        """
        output = search_tool.invoke({"query": state["input"]})
        return {"search_results": output}

    def should_generate(self, state: AgentState) -> str:
        """Determine if the search results are relevant for query before generating a response.

        Args:
            state (AgentState): The state of the agent

        Raises:
            ValueError: Invalid output from search_content_evaluator

        Returns:
            str: The decision to generate a response or not
        """
        chain = search_content_evaluator(self.llm)
        output = chain.invoke(
            {"context": state["search_results"], "query": state["input"]}
        )
        if isinstance(output, BaseModel):
            return output.decision
        else:
            raise ValueError("Invalid output from search_content_evaluator")

    def generate_response(self, state: AgentState) -> dict[str, AIMessage]:
        """Generate a response to the user's query.

        Args:
            state (AgentState): The state of the agent

        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        chain = rag_agent(self.llm)
        output = chain.invoke(
            {
                "context": state["search_results"],
                "query": state["input"],
                "chat_history": state["chat_history"],
            }
        )
        if state.get("images_analysis") is not None:
            return {
                "agent_outcome": AIMessage(
                    content=[{**state["images_analysis"].dict(), **output[0]["args"]}]
                )
            }

        return {"agent_outcome": AIMessage(content=[output[0]["args"]])}

    def agric_specialist_node(self, state: AgentState) -> dict[str, AIMessage]:
        """Where the search results are not relevant, refer the user to another agent.

        Args:
            state (AgentState): The state of the agent

        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        chain = farm_llm(self.llm)
        output = chain.invoke(
            {"input": state["input"], "chat_history": state["chat_history"]}
        )
        return {"agent_outcome": output}

    def fallback_node(self, state: AgentState) -> dict[str, AIMessage]:
        """Fallback to the default response when the search results are not farm or agriculture-related.

        Args:
            state (AgentState): The state of the agent
        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        chain: Runnable = fallback_response(self.llm)
        output: AIMessage = chain.invoke(
            {"input": state["input"], "chat_history": state["chat_history"]}
        )
        return {"agent_outcome": output}


def compile_graph(llm: Optional[BaseChatModel] = None) -> Runnable:
    """Compile the agent workflow graph into langchain runnable.

    Args:
        llm (Optional[BaseChatModel], optional): The language model to use. Defaults to None.

    Returns:
        Runnable: The compiled agent workflow
    """
    nodes = AgentNodes(llm=llm)
    graph = StateGraph(AgentState)
    graph.add_node("search_engine", nodes.search_engine_node)
    graph.add_node("generate_response", nodes.generate_response)
    graph.add_node("agric_specialist", nodes.agric_specialist_node)
    graph.add_node("fallback_node", nodes.fallback_node)
    graph.add_node("crop_disease", nodes.crop_disease_node)
    graph.add_node("crop_pest", nodes.crop_pest_node)
    graph.add_node("unrelated_image", nodes.unrelated_image_node)
    graph.set_conditional_entry_point(
        nodes.router,
        {
            "Yes": "search_engine",
            "No": "fallback_node",
            "pest": "crop_pest",
            "disease": "crop_disease",
            "other": "unrelated_image",
        },
    )
    graph.add_conditional_edges(
        "search_engine",
        nodes.should_generate,
        {"relevant": "generate_response", "not relevant": "agric_specialist"},
    )
    graph.add_edge("crop_disease", "search_engine")
    graph.add_edge("crop_pest", "search_engine")
    graph.add_edge("generate_response", END)
    graph.add_edge("agric_specialist", END)
    graph.add_edge("fallback_node", END)
    graph.add_edge("unrelated_image", END)
    app = graph.compile() | (lambda x: x["agent_outcome"])
    return app
