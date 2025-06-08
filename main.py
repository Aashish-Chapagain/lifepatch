from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_home():
    return FileResponse("static/index.html")

model = OllamaLLM(model="mistral")

template = """You are an intelligent chatbot with sole purpose to reply to the health related questions asked by the users.
chat_history : {history}
You: {input}
"""

prompt = ChatPromptTemplate.from_template(template)
chain_with_memory = prompt | model

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversation = RunnableWithMessageHistory(
    runnable=chain_with_memory,
    get_session_history=get_session_history,
    history_messages_key="history",
    input_messages_key="input",
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    response = conversation.invoke(
        {"input": req.message},
        config={"configurable": {"session_id": req.session_id}},
    )
    return {"response": response}
