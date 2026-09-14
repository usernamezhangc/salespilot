from salespilot.repository import search_products, search_knowledge
from salespilot.embedding import embed_text

class ProductService:
    def search_product(self, keyword:str) -> list:
        return search_products(keyword)

class KnowledgeService:
    def search(self, query: str, top_k: int = 3) -> list:
        vec = embed_text(query)
        return search_knowledge(vec, top_k)
