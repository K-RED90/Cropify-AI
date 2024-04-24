from typing import TypedDict, Optional
from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, root_validator
from langchain_core.language_models import BaseChatModel
from farmGPT.core import (
    input_validator,
    search_content_evaluator,
    farm_llm,
    rag_agent,
    fallback_response,
)
from farmGPT.tools import search_tool
from langchain_core.runnables import Runnable


class AgentState(TypedDict):
    input: str | BaseMessage
    chat_history: list[BaseMessage]
    search_results: Optional[str] = None
    agent_outcome: AIMessage


class AgentNodes(BaseModel):
    llm: Optional[BaseChatModel] = None

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
        return values

    def input_validator_node(self, state: AgentState):
        """Validate the user's input to determine if it is farm-related or not.

        Args:
            state (AgentState): The state of the agent

        Returns:
            str: The output of the validation
        """
        chain = input_validator(self.llm)
        output = chain.invoke(state)
        return output.is_farm_related

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
    graph.set_conditional_entry_point(
        nodes.input_validator_node, {"Yes": "search_engine", "No": "fallback_node"}
    )
    graph.add_conditional_edges(
        "search_engine",
        nodes.should_generate,
        {"relevant": "generate_response", "not relevant": "agric_specialist"},
    )
    graph.add_edge("generate_response", END)
    graph.add_edge("agric_specialist", END)
    graph.add_edge("fallback_node", END)
    app = graph.compile() | (lambda x: x["agent_outcome"])
    return app
