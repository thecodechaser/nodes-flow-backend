from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
import networkx as nx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Edge(BaseModel):
    source: str
    target: str

class PipelineRequest(BaseModel):
    nodes: List[Dict]
    edges: List[Edge]

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post("/pipelines/parse")
async def parse_pipeline(payload: PipelineRequest):
    num_nodes = len(payload.nodes)
    num_edges = len(payload.edges)

    G = nx.DiGraph()
    for node in payload.nodes:
        G.add_node(node["id"])
    for edge in payload.edges:
        G.add_edge(edge.source, edge.target)

    is_dag = nx.is_directed_acyclic_graph(G)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag
    }
