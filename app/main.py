from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, Dict
import os
from dotenv import load_dotenv

load_dotenv()

from notion_client import Client

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
if not NOTION_TOKEN:
    raise RuntimeError("NOTION_TOKEN not found in environment. Please set it in .env or env vars")

notion = Client(auth=NOTION_TOKEN)

app = FastAPI(title="Notion API for ChatGPT Actions",
              description="A lightweight wrapper around Notion API for ChatGPT Actions and OpenWebUI tools",
              version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreatePageRequest(BaseModel):
    parent_database_id: Optional[str]
    properties: Dict[str, Any]
    children: Optional[Any] = None

class UpdatePageRequest(BaseModel):
    properties: Optional[Dict[str, Any]] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/databases")
async def list_databases():
    try:
        resp = notion.search(filter={"property": "object", "value": "database"})
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/databases/{database_id}/rows")
async def list_database_rows(database_id: str = Path(..., description="Notion Database ID"),
                             page_size: int = 50):
    try:
        resp = notion.databases.query(database_id=database_id, page_size=page_size)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/pages/{page_id}")
async def get_page(page_id: str = Path(..., description="Notion Page ID")):
    try:
        page = notion.pages.retrieve(page_id=page_id)
        blocks = notion.blocks.children.list(block_id=page_id)
        return {"page": page, "blocks": blocks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/pages")
async def create_page(req: CreatePageRequest):
    try:
        payload = {
            "parent": {"database_id": req.parent_database_id} if req.parent_database_id else {"type": "page_id"},
            "properties": req.properties
        }
        if req.children:
            payload["children"] = req.children
        resp = notion.pages.create(**payload)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/v1/pages/{page_id}")
async def update_page(page_id: str, req: UpdatePageRequest):
    try:
        if not req.properties:
            raise HTTPException(status_code=400, detail="No properties provided")
        resp = notion.pages.update(page_id=page_id, properties=req.properties)
        return resp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
