import nest_asyncio
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
import uvicorn
from crew import AgenticRagCrew

nest_asyncio.apply()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crew = AgenticRagCrew()

@app.get("/")
def serve_html():
    return FileResponse("index.html")

@app.get("/api/{any_agent}")  
def run_agent(any_agent: str, query: str = Query(...)):
    try:
        # filters = crew.extract_filters_from_query(query)
        result = crew.run_task_by_classified_intent(query)
        return result
    except Exception as e:
        return {"error": str(e)}

tunnel = ngrok.connect(8000)
public_url = tunnel.public_url
print(f" Open the HTML UI here: {public_url}")

with open("index.html", "r") as f:
    html = f.read().replace("https://388d-34-125-10-21.ngrok-free.app", public_url)

with open("index.html", "w") as f:
    f.write(html)

uvicorn.run(app, port=8000)
