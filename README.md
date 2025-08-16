# Basir_RAG_Agents

## RAGAgents

Lightweight Python Retrieval-Augmented Generation agents using LangChain + Ollama, Weaviate vector DB, and Pydantic schemas. Includes ingestion helpers, a FastAPI UI and ngrok tunnel for quick demos.

## Key tools

- LangChain (agent orchestration)
- Ollama (local LLM backend; `llama3` in code)
- Weaviate (vector database for embeddings/search)
- sentence-transformers (embedding model / vectorizer)
- Pydantic (output schemas and validation)
- FastAPI + Uvicorn (HTTP API and server)
- MongoDB (optional data source; connection code present)
- ngrok / pyngrok (exposes local UI for demos)
- Crewai (agent/dataset tooling; referenced in requirements)

## Core components

- `langchain_crew.py` — builds a LangChain React-style agent using `OllamaLLM`, a custom `WeaviateSearch` tool (searches collections and returns JSON), and Pydantic output schemas for activities/restaurants.
- `tools/weaviate_tools/` — vectorizer, insert and retrieval helpers used to populate Weaviate.
- `tools/mongodb_tools/` — utilities to fetch data from MongoDB if used as a source.
- `main.py` — FastAPI app that loads `AgenticRagCrew` from `crew.py`, serves the front-end and exposes the API; auto-updates `index.html` with the ngrok public URL.
- `agents/` — YAML agent/task configs.

## Outputs & data

- `json_results/` — example query results and combined evaluation outputs
- `*_result.json` — sample data files used by ingestion scripts

## Notes

- The project expects local or cloud instances of Ollama and Weaviate; check `config/` for connection helpers.
- `requirements.txt` lists pinned libraries used across the codebase.
