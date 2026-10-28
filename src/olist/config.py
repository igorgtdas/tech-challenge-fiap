"""Caminhos do projeto e o "dicionário" das tabelas do dataset Olist.

Tudo que descreve o dataset (arquivo, chave, granularidade, relações) fica aqui,
para que notebook, Excel e Word usem exatamente as mesmas definições.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
EXCEL_PATH = REPORTS / "indicadores_olist.xlsx"
JSON_PATH = REPORTS / "indicadores.json"

# nome curto -> arquivo, chave primária, granularidade (1 linha = ...) e colunas de data
TABLES = {
    "customers": {
        "file": "olist_customers_dataset.csv",
        "key": ["customer_id"],
        "grain": "1 linha por cliente-em-um-pedido (o mesmo cliente real recebe um customer_id novo a cada pedido)",
        "dates": [],
    },
    "orders": {
        "file": "olist_orders_dataset.csv",
        "key": ["order_id"],
        "grain": "1 linha por pedido",
        "dates": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    },
    "order_items": {
        "file": "olist_order_items_dataset.csv",
        "key": ["order_id", "order_item_id"],
        "grain": "1 linha por item dentro do pedido",
        "dates": ["shipping_limit_date"],
    },
    "payments": {
        "file": "olist_order_payments_dataset.csv",
        "key": ["order_id", "payment_sequential"],
        "grain": "1 linha por forma de pagamento usada no pedido",
        "dates": [],
    },
    "order_reviews": {
        "file": "olist_order_reviews_dataset.csv",
        "key": ["review_id", "order_id"],
        "grain": "1 linha por avaliação ligada a um pedido (há pedidos com mais de uma)",
        "dates": ["review_creation_date", "review_answer_timestamp"],
    },
    "products": {
        "file": "olist_products_dataset.csv",
        "key": ["product_id"],
        "grain": "1 linha por produto",
        "dates": [],
    },
    "sellers": {
        "file": "olist_sellers_dataset.csv",
        "key": ["seller_id"],
        "grain": "1 linha por vendedor",
        "dates": [],
    },
    "geolocation": {
        "file": "olist_geolocation_dataset.csv",
        "key": ["geolocation_zip_code_prefix"],
        "grain": "1 linha por ponto de coordenada (o mesmo CEP aparece várias vezes)",
        "dates": [],
    },
    "category_translation": {
        "file": "product_category_name_translation.csv",
        "key": ["product_category_name"],
        "grain": "1 linha por categoria (tradução para inglês)",
        "dates": [],
    },
}

# Colunas lidas como texto: CEPs (zeros à esquerda) e identificadores.
TEXT_COLUMNS = {
    "customer_zip_code_prefix",
    "seller_zip_code_prefix",
    "geolocation_zip_code_prefix",
}

# (tabela filha, coluna, tabela pai, coluna) — usado no diagrama e na integridade referencial
RELATIONS = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
    ("order_items", "seller_id", "sellers", "seller_id"),
    ("payments", "order_id", "orders", "order_id"),
    ("order_reviews", "order_id", "orders", "order_id"),
    ("customers", "customer_zip_code_prefix", "geolocation", "geolocation_zip_code_prefix"),
    ("sellers", "seller_zip_code_prefix", "geolocation", "geolocation_zip_code_prefix"),
    ("products", "product_category_name", "category_translation", "product_category_name"),
]

# As 8 tabelas citadas no enunciado (p. 3–4); a tradução de categorias é apoio.
ENUNCIADO_TABLES = [
    "customers", "orders", "order_items", "payments",
    "order_reviews", "products", "sellers", "geolocation",
]
