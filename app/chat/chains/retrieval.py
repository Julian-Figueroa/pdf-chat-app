from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable import StreamableChain


class StreamingConversationalRetrievalChain(
    StreamableChain, ConversationalRetrievalChain
):
    """
    A streaming version of the ConversationalRetrievalChain that supports
    streaming responses.
    """

    pass
