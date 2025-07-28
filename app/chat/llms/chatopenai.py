from langchain.chat_models import ChatOpenAI


def build_llm(chat_args, model_name):
    """
    Build a language model for the chat.

    :param chat_args: ChatArgs object containing conversation_id.
    :return: A ChatOpenAI object.
    """
    return ChatOpenAI(streaming=chat_args.streaming, model_name=model_name)
