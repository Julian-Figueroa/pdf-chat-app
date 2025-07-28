from langchain.memory import ConversationBufferMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory


def window_buffer_memory_builder(chat_args) -> ConversationBufferMemory:
    """
    Build a memory object for the chat with window buffer.

    :param chat_args: ChatArgs object containing conversation_id.
    :return: A ConversationBufferMemory object.
    """
    return ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        return_messages=True,
        output_key="answer",
        k=2,
    )
