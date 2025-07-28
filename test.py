from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # print(token, end="", flush=True)
        self.queue.put(token)

    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)

    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)


chat = ChatOpenAI(streaming=True)
prompt = ChatPromptTemplate.from_messages([("human", "{content}")])

# chain = LLMChain(llm=chat, prompt=prompt)
# output = chain("Tell me a small joke!")
# input = {"content": "Tell me a small joke!"}
# for output in chain.stream(input=input):
#     print(output, end="", flush=True)
# messages = prompt.format_messages(content="Tell me a small joke!")

# print(messages)
# output = chat.stream(messages)


# Implement streaming
# class StreamingLLMChain(LLMChain):
class StreamableChain:
    def stream(self, input: dict):
        queue = Queue()
        handler = StreamingHandler()

        def task():
            # This is to ensure that the queue is cleared before starting
            self(input, callbacks=[handler])

        Thread(target=task).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token


class StreamingLLMChain(StreamableChain, LLMChain):
    pass


chain = StreamingLLMChain(llm=chat, prompt=prompt)
input = {"content": "Tell me a small joke!"}
for output in chain.stream(input=input):
    print(output, end="", flush=True)
