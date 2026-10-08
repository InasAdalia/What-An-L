# Script 03 — Chatbot with Memory
# A real chatbot that remembers what was said earlier in the conversation.
#
# Key insight: LLMs are stateless by nature — every .invoke() is independent.
# Memory = you manually keep the message history and pass it with every call.
# This is the same "stateful vs stateless" concept from your SBOD integration tests.
#
# [LC] Official docs — Chat History: https://python.langchain.com/docs/concepts/chat_history/
# [LC] Official docs — How to add memory: https://python.langchain.com/docs/how_to/chatbot_memory/

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# ── 1. Model ─────────────────────────────────────────────────
llm = ChatOllama(model="llama3.2:3b")

# ── 2. Prompt with a MessagesPlaceholder ─────────────────────
# [LC] MessagesPlaceholder is a special placeholder that inserts a *list* of messages
#      into the prompt. This is where the conversation history gets injected.
#
#      The full prompt sent to the LLM each turn looks like:
#        [SystemMessage, HumanMessage(turn1), AIMessage(turn1), HumanMessage(turn2), ...]
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Be concise."),
    MessagesPlaceholder(variable_name="history"),  # ← conversation history goes here
    ("human", "{input}"),                          # ← current user message
])

# ── 3. Chain ─────────────────────────────────────────────────
chain = prompt | llm | StrOutputParser()

# ── 4. Memory storage ────────────────────────────────────────
# [LC] LangChain has built-in memory classes, but the simplest approach is:
#      just maintain a Python list of messages yourself.
#      Each turn: append HumanMessage, get response, append AIMessage.
#
# [PY] [] is an empty list — we'll .append() to it each turn
history = []

# ── 5. Chat loop ─────────────────────────────────────────────
# [PY] `while True` = loop forever until we explicitly `break` out
print("Chatbot with memory — type 'quit' to exit\n")

while True:
    # [PY] input() reads a line from the terminal
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Bye!")
        break

    # [LC] Pass the current history + the new user message to the chain
    response = chain.invoke({
        "history": history,
        "input": user_input,
    })

    print(f"AI : {response}\n")

    # [LC] After each turn, append BOTH messages to history so the next turn
    #      has full context. This is the "memory" — it's just a list.
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))

    # Peek at what's in memory (remove this once you understand it)
    print(f"  [debug] history length: {len(history)} messages\n")


# ─────────────────────────────────────────────────────────────
# Try it yourself:
#
# 1. Start the chatbot. Say: "My name is Inas."
#    Then ask: "What is my name?"
#    Does it remember? It should.
#
# 2. Add a history limit — only keep the last 10 messages:
#    history = history[-10:]   (add this line after appending)
#    This prevents the prompt from getting too long. Why does that matter?
#
# 3. Print the full history list at the end (after typing quit).
#    Notice the alternating HumanMessage / AIMessage pattern.
#    This is exactly what gets sent to the LLM on each turn.
# ─────────────────────────────────────────────────────────────
