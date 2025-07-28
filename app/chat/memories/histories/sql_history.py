from pydantic import BaseModel, Field
from langchain.schema import BaseChatMessageHistory

from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation,
)


class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    """
    Custom message history that stores messages in a SQL database.
    """

    conversation_id: str = Field(..., description="The ID of the conversation")

    @property
    def messages(self) -> None:
        """
        Get messages history.
        """
        return get_messages_by_conversation_id(self.conversation_id)

    def add_message(self, message) -> None:
        """
        Add a message to the conversation.
        """
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content,
        )

    def clear(self) -> None:
        """Clear the message history."""
        # raise NotImplementedError(
        #     "Clear method is not implemented for SQL message history."
        # )
        pass
