from typing import TypedDict, Optional, Type, Callable, Union, Dict, Annotated
from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel, root_validator
from langchain_core.language_models import BaseChatModel
from .core import (
    input_validator,
    evaluator,
    farm_chain,
    pest_and_disease_tool,
    Pest,
    Disease,
    PestOrDisease,
    specialist_chain,
)
from .prompts import (
    PEST_PROMPT,
    DISEASE_PROMPT,
    IMAGE_CLASSIFICATION_PROMPT,
    DEFAULT_MESSAGE,
    SEARCH_QUERIES_PROMPT,
    RESPONSE_WRITER,
    EVALUATION_PROMPT,
    ANSWER_REFINER,
    METEOROLOGIST_PROMPT,
    FALLBACK_PROMPT,
)
from langchain_core.runnables import Runnable
from functools import partial
from logger import log_function_time
from .utils import encode_image, json_to_markdown
from weather_tools import GetWeatherDataByCityName, GetWeatherForecastByCityName
from .tools import CustomDDGSearch, search_tool
from operator import add
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langgraph.prebuilt import ToolInvocation, ToolExecutor
import json
from .schemas import (
    ResponseFormat,
    SearchQueryOutput,
    AnswerEvaluation,
    AnswerRefinement,
)
from collections import defaultdict
from datetime import datetime
from langchain_core.runnables import RunnablePassthrough


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add] = None
    image_path: Optional[str] = None
    chat_history: list[BaseMessage]
    search_results: Optional[str]
    evaluation: Optional[dict]
    farmer_query: Optional[str]
    agent_outcome: Union[AIMessage, Type[BaseModel], Dict]
    images_analysis: Type[BaseModel] | Dict = None


class AgentNodes(BaseModel):
    llm: Optional[BaseChatModel] = None
    chain: Optional[Runnable] = None
    vision_tool: Optional[Callable] = None
    tool_executor: Optional[ToolExecutor] = None
    parser: Optional[JsonOutputToolsParser] = JsonOutputToolsParser(return_id=True)

    @root_validator
    def check_llm(cls, values):
        llm = values.get("llm")
        vision_tool = values.get("vision_tool")
        if llm is None:
            try:
                from langchain_openai.chat_models import ChatOpenAI
            except ImportError:
                raise ImportError(
                    "Please install the openai plugin to use the default LLM. Run `pip install langchain-openai`"
                )
            llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)
            # vision_model = ChatOpenAI(model="gpt-4-vision-preview", temperature=0.5)

        if vision_tool is None:
            try:
                from langchain_anthropic.chat_models import ChatAnthropic
            except ImportError:
                raise ImportError(
                    "Please install the anthropic plugin to use the default LLM. Run `pip install langchain-anthropic`"
                )
            vision_model = ChatAnthropic(
                model="claude-3-haiku-20240307", temperature=0.5
            )  #TODO Change to gpt-4-turbo
        
        values["vision_tool"] = partial(pest_and_disease_tool, llm=vision_model)
        values["llm"] = llm
        values["chain"] = partial(farm_chain, llm=llm)
        values["tool_executor"] = ToolExecutor(
            tools=[
                search_tool,
                GetWeatherDataByCityName(),
                GetWeatherForecastByCityName(),
            ]
        )
        return values

    class Config:
        arbitrary_types_allowed = True

    @log_function_time
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
            elif output.label == "crop_disease":
                return "disease"
            else:
                return "other_image"
        else:
            chain = input_validator(self.llm)
            output = chain.invoke(
                {"messages": state["messages"], "chat_history": state["chat_history"]}
            )
            return output.route

    def queries_writer(self, state: AgentState):
        chain = self.chain(
            system_prompt=SEARCH_QUERIES_PROMPT, tools=[SearchQueryOutput]
        )
        print("===Writing queries===")
        response = chain.invoke(state)
        return {"messages": [response]}

    @log_function_time
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
            "images_analysis": output.dict(),
            "messages": [
                HumanMessage(
                    content=f"What are the treatment OR control of {str(output.disease)}"
                )
            ],
        }

    @log_function_time
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
            "images_analysis": output.dict(),
            "messages": [
                HumanMessage(
                    content=f"What are the treatment OR control of {str(output.pest)}"
                )
            ],
        }

    @log_function_time
    def unrelated_image_node(self, state: AgentState) -> dict[str, AIMessage]:
        """When the image is not related to crop pests or diseases.

        Args:
            state (AgentState): The state of the agent

        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        return {"messages": [AIMessage(content=DEFAULT_MESSAGE)]}

    def meteorologist(self, state: AgentState):
        chain = RunnablePassthrough.assign(
            location=lambda x: "Accra,GH",
            date_time=lambda x: datetime.now().strftime("%A, %B %d, %Y %H:%M:%S"),
        ) | self.chain(
            system_prompt=METEOROLOGIST_PROMPT,
            tools=[GetWeatherDataByCityName(), GetWeatherForecastByCityName()],
        )
        print("===Getting Weather Forecast===")
        response = chain.invoke(
            {"messages": state["messages"], "chat_history": state["chat_history"]}
        )
        return {"messages": [response]}

    def call_tools(self, state: AgentState):
        agent_actions = self.parser.invoke(state["messages"][-1])
        # print(agent_actions)
        print("===Calling Tools===")
        ids = []
        tool_invocations = []
        for tool_call in agent_actions:
            if tool_call["args"].get("search_queries") is not None:
                for query in tool_call["args"]["search_queries"]:
                    tool_invocations.append(
                        ToolInvocation(
                            tool="search_engine",
                            tool_input=query,
                        )
                    )
                    ids.append(tool_call["id"])
            else:
                tool_invocations.append(
                    ToolInvocation(tool=tool_call["type"], tool_input=tool_call["args"])
                )
                ids.append(tool_call["id"])
        tool_results = self.tool_executor.batch(tool_invocations)
        output_map = defaultdict(dict)
        for id_, output, action in zip(ids, tool_results, tool_invocations):
            output_map[id_][json.dumps(action.tool_input)] = output
        return {
            "messages": [
                ToolMessage(content=json.dumps(output), tool_call_id=id_)
                for id_, output in output_map.items()
            ],
            "farmer_query": agent_actions[0]["args"].get("farmer_query"),
        }

    def should_continue(self, state: AgentState):
        if not self.parser.invoke(state["messages"][-1]):
            return "end"
        return "continue"

    def answer_writer(self, state: AgentState):
        chain: Runnable = self.chain(
            system_prompt=RESPONSE_WRITER,
            tools=[ResponseFormat],
            tool_choice=ResponseFormat.__name__,
        )
        print("===Writing answer===")
        response: AIMessage = chain.invoke(
            {"messages": state["messages"], "chat_history": state["chat_history"]}
        )
        response = self.parser.invoke(response)

        return {
            "messages": [
                AIMessage(
                    content=response[0]["args"]["answer"],
                    response_metadata={"links": response[0]["args"]["links"]},
                    name="answer_writer",
                )
            ]
        }

    def answer_evaluator(self, state: AgentState):
        chain = evaluator(
            llm=self.llm, prompt_template=EVALUATION_PROMPT, tool=AnswerEvaluation
        )
        print("===Evaluating answer===")
        ai_answer = state["messages"][-1]
        output = chain.invoke(
            {"ai_answer": ai_answer.content, "farmer_query": state["farmer_query"]}
        )
        output = self.parser.invoke(output)[0]["args"]
        return {"evaluation": output}

    def should_go_to_specialist(self, state: AgentState):
        if state["evaluation"]["evaluation"] == "partially_complete":
            return "yes"
        return "no"

    @log_function_time
    def agric_specialist(self, state: AgentState) -> dict[str, AIMessage]:

        chain: Runnable = specialist_chain(
            llm=self.llm,
            system_prompt=ANSWER_REFINER,
            tools=[AnswerRefinement],
            tool_choice=AnswerRefinement.__name__,
        )
        print("===Calling Specialist===")
        previous_answer = state["messages"][-1]
        response = chain.invoke(
            {
                "query": state["farmer_query"],
                "previous_answer": previous_answer.content,
                "feedback": state["evaluation"]["feedback"],
            }
        )
        response = self.parser.invoke(response)[0]["args"]

        return {
            "agent_outcome": AIMessage(
                content=response["answer"],
                response_metadata=previous_answer.response_metadata,
                name="agric_specialist",
            )
        }

    def format_response(self, state: AgentState):
        response = state["messages"][-1]
        images_analysis = state.get("images_analysis")

        if images_analysis is not None:
            images_response = json_to_markdown(images_analysis)
            response = AIMessage(
                content=f"{images_response}\n\n**Control/Treatment:** {response.content}",
                response_metadata=response.response_metadata,
                name="final",
            )
        return {"agent_outcome": response}

    @log_function_time
    def fallback_node(self, state: AgentState) -> dict[str, AIMessage]:
        """Fallback to the default response when the search results are not farm or agriculture-related.

        Args:
            state (AgentState): The state of the agent
        Returns:
            dict[str, AIMessage]: The response to the user's query
        """
        chain: Runnable = self.chain(system_prompt=FALLBACK_PROMPT)
        output: AIMessage = chain.invoke(state)
        return {"messages": [output]}


def compile_graph(llm: Optional[BaseChatModel] = None) -> Runnable:
    """Compile the agent workflow graph into langchain runnable.

    Args:
        llm (Optional[BaseChatModel], optional): The language model to use. Defaults to None.

    Returns:
        Runnable: The compiled agent workflow
    """
    nodes = AgentNodes(llm=llm)
    graph = StateGraph(AgentState)
    graph.add_node("search_tool", nodes.call_tools)
    graph.add_node("weather_tools", nodes.call_tools)
    graph.add_node("queries_writer", nodes.queries_writer)
    graph.add_node("answer_writer", nodes.answer_writer)
    graph.add_node("answer_evaluator", nodes.answer_evaluator)
    graph.add_node("specialist", nodes.agric_specialist)
    graph.add_node("meteorologist", nodes.meteorologist)
    graph.add_node("final", nodes.format_response)
    graph.add_node("diseases_specialist", nodes.crop_disease_node)
    graph.add_node("pests_specialist", nodes.crop_pest_node)
    graph.add_node("unrelated_image", nodes.unrelated_image_node)
    graph.add_node("fallback", nodes.fallback_node)
    graph.set_conditional_entry_point(
        nodes.router,
        {
            "farm_query": "queries_writer",
            "weather": "meteorologist",
            "other": "fallback",
            "pest": "pests_specialist",
            "disease": "diseases_specialist",
            "other_image": "unrelated_image",
        },
    )
    graph.add_conditional_edges(
        "meteorologist",
        nodes.should_continue,
        {"end": "final", "continue": "weather_tools"},
    )
    graph.add_edge("weather_tools", "meteorologist")
    graph.add_edge("diseases_specialist", "queries_writer")
    graph.add_edge("pests_specialist", "queries_writer")
    graph.add_edge("queries_writer", "search_tool")
    graph.add_edge("search_tool", "answer_writer")
    graph.add_edge("answer_writer", "answer_evaluator")
    graph.add_conditional_edges(
        "answer_evaluator",
        nodes.should_go_to_specialist,
        {"yes": "specialist", "no": "final"},
    )
    graph.add_edge("specialist", "final")
    graph.add_edge("unrelated_image", "final")
    graph.add_edge("fallback", "final")
    graph.add_edge("final", END)
    app = graph.compile() | (lambda x: x["agent_outcome"])
    return app
