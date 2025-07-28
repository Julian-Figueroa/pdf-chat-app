from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import set_conversation_components, get_conversation_components
from app.chat.score import random_component_by_score


def select_component(component_type: str, component_map, chat_args: ChatArgs):
    components = get_conversation_components(chat_args.conversation_id)

    previous_component = components[component_type]
    if previous_component:
        # this is NOT the first message in the conversation
        # and we need to use the same retriever again
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        # this is the first message in the conversation
        # and we need to picka random retriever
        random_component_name = random_component_by_score(component_type, component_map)
        print(f"Selected random {component_type}: {random_component_name}")
        builder = component_map[random_component_name]
        return random_component_name, builder(chat_args)
        # set_conversation_components(
        #     conversation_id=chat_args.conversation_id,
        #     llm="",
        #     memory="",
        #     retriever=random_component_name,
        # )


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    # retriever = retriever_map(chat_args)
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)

    # print(f"Using LLM: {llm_name}, Memory: {memory_name}, Retriever: {retriever_name}")

    # Set the conversation components
    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        llm=llm_name,
        memory=memory_name,
        retriever=retriever_name,
    )

    # llm = build_llm(chat_args)
    # memory = build_memory(chat_args)
    condense_question_llm = ChatOpenAI(streaming=False)

    # Create trace
    # trace = langfuse.create_trace(
    #     conversation_id=chat_args.conversation_id, metadata=chat_args.metadata
    # )

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        condense_question_llm=condense_question_llm,
    )
