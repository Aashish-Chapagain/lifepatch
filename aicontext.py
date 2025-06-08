from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory 



model = OllamaLLM(model = "mistral")


template = ("""You are an intelligent chatbot with sole purpose to reply to the health related questions asked by the users.
            chat_history : {history}
            You: {input}""")


prompt =  ChatPromptTemplate.from_template(template)



chain_with_memory = prompt | model 

store  = {}

def get_session_history(session_id: str):
    if session_id not in store: 
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]



conversation = RunnableWithMessageHistory(
    runnable=chain_with_memory,
    get_session_history = get_session_history,
    history_messages_key="history",
    input_messages_key="input",
)
print("Welcome to the Health Chatbot! Type 'exit' to end the conversation.")

while True : 
 user_input = input("you: ").lower().strip()
 if user_input in ["exit", "quit", "stop"]:
        print("Ending the conversation. Goodbye!")
        break
 response = conversation.invoke({"input" : user_input},
                                config={"configurable": {"session_id": "user_1"}})
 print("Bot:", response)