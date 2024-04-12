def load_llm(model: str = "gpt-3.5-turbo-0125", temperature=0.0):
    try:
        from langchain_openai.chat_models import ChatOpenAI
    except ImportError:
        raise ImportError(
            "Please, install langchain_openai. `pip install langchain-openai`"
        )
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        model_kwargs={"stop": ["Please, Note", "It is important"]},
    )
