# Script 02 — PromptTemplate + LCEL Chain
# Instead of building messages manually, use a template with placeholders.
# Then chain it together with the LLM using the `|` pipe operator.
#
# [LC] Official docs — Prompt Templates: https://python.langchain.com/docs/concepts/prompt_templates/
# [LC] Official docs — LCEL:             https://python.langchain.com/docs/concepts/lcel/

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── 1. The Model ─────────────────────────────────────────────
llm = ChatOllama(model="llama3.2:3b")

# ── 2. The Prompt Template ───────────────────────────────────
# [LC] ChatPromptTemplate.from_messages() takes a list of (role, content) tuples.
#      {topic} and {level} are placeholders — like `{variable}` in a Thymeleaf template.
#
#      Roles:
#        "system"    → sets the AI's behaviour/persona (developer-controlled)
#        "human"     → the user's message
#        "assistant" → a previous AI response (used when you want few-shot examples)
#
# [PY] A tuple is (item1, item2) — like an immutable array of fixed length.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical educator. Explain concepts clearly and concisely."),
    ("human", "Explain {topic} to someone who is a {level} developer. Explain in a {style} tone"),
])

# ── 3. The Output Parser ─────────────────────────────────────
# [LC] StrOutputParser just extracts the text from the AIMessage response.
#      Without it, .invoke() returns an AIMessage object.
#      With it, .invoke() returns a plain string.
parser = StrOutputParser()

# ── 4. The Chain (LCEL) ──────────────────────────────────────
# [LC] The `|` pipe operator connects components left to right.
#      Output of left becomes input of right — like piping in a terminal.
#
#      prompt | llm | parser means:
#        1. prompt.invoke(inputs)   → formats into a list of messages
#        2. llm.invoke(messages)    → sends to model, returns AIMessage
#        3. parser.invoke(message)  → extracts .content as plain string
#
# [PY] This creates a "Runnable" object — you call .invoke() on it just like on the individual pieces.
chain = prompt | llm | parser
# chain = prompt | llm


# ── 5. Run the chain ─────────────────────────────────────────
# [LC] Pass a dict with values for each placeholder in the prompt template.
result = (prompt | llm | parser).invoke({
    "topic": "vector embeddings",
    "level": "junior web",
    "style" : "humorous"
})

# without parser, since output will be in AIMessage object, can do result.content
# with parser, it seems like only content is being shown, and formatted like md file
print(result)

# ─────────────────────────────────────────────────────────────
# Try it yourself:
#
# 1. Add a third placeholder {style} and use it in the system prompt:
#    "Explain in a {style} tone."
#    Then pass style="humorous" in the .invoke() dict.
#
# 2. Change the chain to NOT use the parser. Print the result — what type is it?
#    response = (prompt | llm).invoke({...})
#    print(type(response))
#
# 3. Try chain.batch([...]) — pass a list of dicts to run multiple inputs at once.
#    Docs: https://python.langchain.com/docs/concepts/lcel/#batch
# ─────────────────────────────────────────────────────────────
