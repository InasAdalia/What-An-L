# Script 01 — Hello LLM
# The most basic thing: send a message to a model, get a response back.
#
# [LC] Official docs: https://python.langchain.com/docs/concepts/chat_models/
# [LC] Ollama integration: https://python.langchain.com/docs/integrations/chat/ollama/

# [PY] "from X import Y" = like `import { Y } from 'X'` in TypeScript
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# [LC] ChatOllama is a "ChatModel" — a wrapper around the Ollama API.
#      All LangChain chat models share the same interface (invoke, stream, batch),
#      so you can swap Ollama for OpenAI/Anthropic/Gemini without changing any other code.
#
# [PY] model="llama3.2:3b" is a keyword argument (like a named parameter)
llm = ChatOllama(model="llama3.2:3b")

# [LC] A "message" tells the LLM WHO is speaking.
#      SystemMessage  = instructions/persona for the AI (the developer sets this)
#      HumanMessage   = what the user typed
#      AIMessage      = what the AI responded (you'll see this in the output)
#
# [PY] A list in Python uses square brackets: [item1, item2]
messages = [
    # SystemMessage(content="You are a pirate. Keep answers to 2 sentences max. Answer in a pirate accent"),
    HumanMessage(content="Why is the sky blue?"),
]

# [LC] .invoke() sends the messages to the model and waits for the full response.
#      The return value is an AIMessage object.
response = llm.invoke(messages)

# [PY] f"..." is a formatted string — like template literals in TypeScript
#      response.content is the text the LLM returned
print(f"Response type : {type(response)}")
print(f"Response text : {response.content}")


# ─────────────────────────────────────────────────────────────
# Try it yourself — modify and re-run:
#
# 1. Change the SystemMessage to make the LLM respond like a pirate.
# 2. Change the HumanMessage to ask something else.
# 3. Try removing the SystemMessage entirely — what changes?
# ─────────────────────────────────────────────────────────────

# [PY] This pattern means: only run the code below when this file is executed directly.
#      (not when it's imported by another file — like the `main` function in Java)
if __name__ == "__main__":
    pass  # [PY] `pass` = do nothing (placeholder)
