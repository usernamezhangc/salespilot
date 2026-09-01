from salespilot.repository import search_products

class ProductService:
    def search_product(self, keyword:str) -> list:
        return search_products(keyword)
