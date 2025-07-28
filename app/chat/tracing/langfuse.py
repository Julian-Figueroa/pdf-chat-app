# app/chat/tracing/langfuse_wrapper.py
import os
from typing import Optional, Dict, Any
from langfuse import Langfuse


class LangfuseWrapper:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            project_name="pdf-project",
        )

    def create_trace(self, conversation_id: str, metadata: Optional[Dict] = None):
        """Version-agnostic trace creation"""
        try:
            # Try new version API (v2+)
            from langfuse import CreateTrace

            return self.langfuse.trace(
                CreateTrace(id=conversation_id, metadata=metadata or {})
            )
        except ImportError:
            # Fallback to old version API (v1)
            return self.langfuse.trace(
                name="pdf-chat", id=conversation_id, metadata=metadata or {}
            )

    def get_handler(self, trace):
        """Version-agnostic handler getter"""
        try:
            return trace.get_langchain_handler()  # New version
        except AttributeError:
            return trace.getNewHandler()  # Old version


# Singleton instance
langfuse = LangfuseWrapper()
