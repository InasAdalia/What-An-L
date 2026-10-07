# LangChain 10-Day Learning Roadmap
> 6 hours/day minimum · Project-based · All work lives in `_personal/`
> always tag resources so that i can learn to use reference while developing
---

## The Plan at a Glance

| Day | Theme | Mini Project |
|-----|-------|--------------|
| 1–2 | LangChain Foundation (ChatModel, Prompt, LCEL, Memory) | Personal assistant chatbot with memory |
| 3–4 | RAG Part 1 — Indexing (Loaders, Splitter, Embeddings, FAISS) | Index fake car telemetry JSON, query it |
| 5–6 | RAG Part 2 — Retrieval & Output (full RAG chain, Output Parsers) | Telemetry Q&A with structured JSON answers |
| 7–8 | Elasticsearch Integration (ES basics, ElasticsearchStore, hybrid search) | Migrate FAISS project → Elasticsearch |
| 9–10 | Agents + LangGraph (Tools, ReAct, state machines) | Multi-tool agent: search + stats + report |

---

## Day 1–2: LangChain Foundation

**What you will understand after this:**
- What a ChatModel is and how to call it
- How PromptTemplate parameterises a prompt
- How LCEL (`|` pipe) chains components
- How Memory makes a chatbot remember past turns

**Mini Project:** A personal assistant chatbot that remembers the conversation.

**Resources:**
- [LangChain Docs — Chat Models](https://python.langchain.com/docs/concepts/chat_models/)
- [LangChain Docs — Prompt Templates](https://python.langchain.com/docs/concepts/prompt_templates/)
- [LangChain Docs — LCEL](https://python.langchain.com/docs/concepts/lcel/)
- [LangChain Docs — Memory / Chat History](https://python.langchain.com/docs/concepts/chat_history/)
- [Ollama model library](https://ollama.com/library)

Work folder: `day-01/`

---

## Day 3–4: RAG Part 1 — Indexing

**What you will understand after this:**
- Document Loaders (JSON, CSV, plain text)
- Text Splitter (chunk_size, chunk_overlap, why it matters)
- Embeddings (converting text to vectors)
- FAISS vector store (local, no server needed)
- Indexing pipeline end-to-end

**Mini Project:** Index 20 fake car telemetry records (JSON), ask natural-language questions against them.

**Resources:**
- [LangChain Docs — Document Loaders](https://python.langchain.com/docs/concepts/document_loaders/)
- [LangChain Docs — Text Splitters](https://python.langchain.com/docs/concepts/text_splitters/)
- [LangChain Docs — Embedding Models](https://python.langchain.com/docs/concepts/embedding_models/)
- [LangChain Docs — Vector Stores](https://python.langchain.com/docs/concepts/vectorstores/)
- [FAISS](https://faiss.ai/)

Work folder: `day-03/`

---

## Day 5–6: RAG Part 2 — Full Retrieval Chain

**What you will understand after this:**
- Retriever abstraction
- Full RAG chain (retriever + prompt + llm + parser)
- Output Parsers — returning structured JSON/Pydantic objects
- Prompt engineering for RAG (system prompts, context injection)

**Mini Project:** Upgrade Day 3 project — answers now return structured JSON with `car_id`, `anomaly_type`, `severity`.

**Resources:**
- [LangChain Docs — Retrievers](https://python.langchain.com/docs/concepts/retrievers/)
- [LangChain Docs — RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [LangChain Docs — Output Parsers](https://python.langchain.com/docs/concepts/output_parsers/)
- [Pydantic docs (v2)](https://docs.pydantic.dev/latest/)

Work folder: `day-05/`

---

## Day 7–8: Elasticsearch Integration

**What you will understand after this:**
- ES index, document, mapping (from an AI perspective)
- Dense vector field + kNN query
- Hybrid search (BM25 keyword + kNN vector)
- ElasticsearchStore in LangChain
- How ECE fits into this picture

**Mini Project:** Migrate the FAISS RAG from Day 3 to a local Elasticsearch instance. Run both BM25 and kNN queries and compare results.

**Resources:**
- [Elasticsearch Docs — What is Elasticsearch?](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html)
- [Elastic Search Labs — RAG with Elasticsearch](https://www.elastic.co/search-labs/blog/rag-with-kibana)
- [LangChain Docs — Elasticsearch integration](https://python.langchain.com/docs/integrations/vectorstores/elasticsearch/)
- [Elasticsearch kNN search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)

Work folder: `day-07/`

---

## Day 9–10: Agents + LangGraph

**What you will understand after this:**
- What a Tool is (a Python function the LLM can call)
- ReAct loop (Reason → Act → Observe)
- LangGraph: nodes, edges, state — same stateful/stateless concept from SBOD
- Human-in-the-loop (agent pauses and asks for approval)

**Mini Project:** Agent that decides whether to search telemetry, calculate stats, or generate a summary report — based on what the user asks.

**Resources:**
- [LangChain Docs — Tools](https://python.langchain.com/docs/concepts/tools/)
- [LangChain Docs — Agents](https://python.langchain.com/docs/concepts/agents/)
- [LangGraph Docs — Get Started](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- [LangChain Academy — LangGraph course (free)](https://academy.langchain.com/courses/intro-to-langgraph)

Work folder: `day-09/`

---

## Things to note as you go (expand on later)

- **LangSmith** — observability/debugging for LangChain apps. Not needed now but note it exists. [langsmith.com](https://smith.langchain.com)
- **LlamaIndex** — alternative to LangChain, more focused on RAG. Worth knowing exists.
- **Multimodal RAG** — CLIP embeddings for images. Relevant if telemetry includes camera feeds.
- **GraphRAG** — knowledge graphs (Neo4j) as retrievers. Mentioned in our ontologies discussion.
- **n8n** — low-code visual AI workflow tool. Different abstraction level than LangChain.

---

## What to ignore for now

- Training/fine-tuning models (PyTorch, Google Colab, Hugging Face Trainer)
- LangChain JS/TS (same concepts, come back later if team uses TypeScript)
- Deep Pydantic theory (just use the patterns)
