from salespilot.knowledge_data import KNOWLEDGE
from salespilot.embedding import embed_text

from salespilot.model import KnowledgeChunk
from salespilot.repository import add_knowledge_chunk

def ingest():
    for item in KNOWLEDGE:
        vec = embed_text(item["content"])
        chunk = KnowledgeChunk(
            title = item["title"],
            content = item["content"],
            embedding = vec,
        )
        add_knowledge_chunk(chunk)
        print(f"已添加： {item['title']}")
    
if __name__ == "__main__":
    ingest()