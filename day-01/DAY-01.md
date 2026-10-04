# Day 1–2: LangChain Foundation

**Goal:** By end of Day 2, you can build a chatbot that:
- Calls a local LLM
- Uses a parameterised prompt
- Remembers the conversation history

**Time split (6h/day):**
- ~1h: Setup
- ~1h: Read through the 3 scripts with the Python annotations
- ~2h: Run each script, modify it, break it, fix it
- ~2h: Mini project (your own version at the bottom of this file)

---

## Step 1 — Install Ollama (your local LLM runner)

Ollama lets you run LLMs on your laptop for free. No API key, no cost.

```bash
brew install ollama
```

Then pull a model. `llama3.2:3b` is 2GB, fast enough for learning:

```bash
ollama pull llama3.2:3b
```

> **Official ref:** https://ollama.com/library/llama3.2 — check the model card to understand what llama3.2 is.

Start the Ollama server (keep this terminal open):

```bash
ollama serve
```

Verify it works (new terminal tab):

```bash
curl http://localhost:11434/api/generate -d '{"model":"llama3.2:3b","prompt":"say hello","stream":false}'
```

You should see a JSON response with a `"response"` field. If yes — Ollama works.

---

## Step 2 — Python virtual environment

A virtual environment isolates your project's dependencies from other Python projects.
Think of it like a separate `node_modules` per project, but for Python.

```bash
cd /Users/IMOHDKH/sbod/_personal
python3 -m venv .venv
source .venv/bin/activate
```

Your terminal prompt should now show `(.venv)` — this means the venv is active.
Run this activation command every time you open a new terminal for this project.

---

## Step 3 — Install packages

```bash
pip install langchain langchain-ollama langchain-community
```

> **Official ref:** https://python.langchain.com/docs/how_to/installation/
>
> `langchain` = core framework
> `langchain-ollama` = Ollama integration (so LangChain can talk to your local model)
> `langchain-community` = third-party integrations (loaders, vector stores, etc.) — needed in later days

---

## Step 4 — Run the scripts in order

```
01_hello_llm.py       ← bare ChatModel call
02_prompt_chain.py    ← add PromptTemplate + LCEL chain
03_chatbot_memory.py  ← add memory (multi-turn conversation)
```

Each script has `# [PY]` comments explaining Python syntax as you encounter it.
Each script has `# [LC]` comments explaining the LangChain concept.

---

## Step 5 — Your Mini Project (Day 2)

### Exercise 1
Build your own version in `my_assistant.py`.

Requirements:
1. System prompt: "You are a helpful assistant for Mercedes-Benz engineers. Answer concisely."
2. Remembers conversation history (multi-turn)
3. When the user types `quit`, it exits
4. Bonus: print how many messages are in the history after each response

You already have all the building blocks from the 3 scripts. Try without looking first.

### Exercise 2
Build a personal study coach chatbot that remembers the user across turns, but keeps the prompt small.
**Problem statement:**
Create an AI assistant for a student that can:
1. remember the student’s name, goal, and preferred explanation style,
2. answer study questions in that style,
3. keep only the last few chat turns in active memory,
4. compress older turns into a short running summary,
5. save that summary to a local file so it can be loaded again after restarting the script.

**Why this is a good next step:**
It goes beyond the 3 examples because you’re not just calling an LLM, templating prompts, or storing a raw message list. You’ll use real LangChain memory patterns: short-term history + memory trimming/summarizing + persistence.
Minimum features:
• ask the user for their name and study goal on first run
• remember those details in later replies
• if conversation gets long, summarize older messages and discard them
• on restart, reload the saved summary and continue

**Keep it simple:**
Don’t add tools, retrieval, agents, or vector DBs yet.
When you write your solution, send it here and I’ll correct it.

---

## Python patterns you will see today (quick reference)

| Pattern | What it means |
|---------|--------------|
| `from x import Y` | Like `import { Y } from 'x'` in TypeScript |
| `def fn(param: str) -> str:` | Function with type hints (like TypeScript) |
| `f"hello {name}"` | Template literal — like `` `hello ${name}` `` |
| `if __name__ == "__main__":` | Entry point — code here only runs when you run this file directly |
| `# comment` | Single-line comment |
| `"""docstring"""` | Multi-line string / doc comment |
| `list = [1, 2, 3]` | Array |
| `dict = {"key": "value"}` | Object / map |
| `for item in list:` | for...of loop |
| `print(x)` | console.log(x) |
