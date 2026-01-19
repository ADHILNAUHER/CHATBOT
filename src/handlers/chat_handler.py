from src.agents.chat_agent.graph import create_chat_agent_graph
from langchain.messages import HumanMessage
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from typing import AsyncGenerator

graph = create_chat_agent_graph()


async def chat_agent_handler(thread_id: str, message: str) -> AsyncGenerator[str, None]:
    """
    Streams the agent's response token by token.
    """
    input_data = {"message": [HumanMessage(content=message)]}
    config = {"configurable": {"thread_id": thread_id}}

    # astream yields events; we filter for 'messages' to get the tokens
    async for event in graph.astream(input_data, config=config, stream_mode="messages"):
        # This extract logic depends on your graph setup,
        # but usually 'messages' mode yields message chunks
        content = event[0].content
        if content:
            yield content


def get_all_threads_handler() -> list[str | None]:
    """ """

    all_checkpoints = graph.checkpointer.list(config={})

    threads = set()

    for checkpoint in all_checkpoints:
        threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(threads)


def chat_history_handler(thread_id: str) -> ChatAgentState | dict[None, None]:
    """"""
    return graph.get_state(config={"configurable": {"thread_id": thread_id}})[0]
