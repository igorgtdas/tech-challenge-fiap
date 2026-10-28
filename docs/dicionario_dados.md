## Dicionário do dataset
Antes de abrir os dados, vale saber o que cada tabela guarda e para que ela serve na análise. O dataset é o *Brazilian E-Commerce Public Dataset by Olist* (Kaggle). Ele tem 8 tabelas citadas no enunciado (p. 3–4) e mais uma de apoio. A Olist anonimizou todos os identificadores (`*_id`): eles servem para ligar as tabelas, não para identificar pessoas.

### Visão geral

| Tabela (arquivo) | O que é | 1 linha representa | Liga com | Para que serve na análise |
|---|---|---|---|---|
| **orders** (`olist_orders_dataset.csv`) | O pedido e as datas do seu ciclo, da compra à entrega | um pedido | customers, order_items, payments, order_reviews | Centro do modelo: volume, status, prazo de entrega e atraso |
| **customers** (`olist_customers_dataset.csv`) | O cliente de cada pedido e onde ele mora | um cliente em um pedido | orders, geolocation | Contar clientes reais, medir recompra e fazer recortes por estado e cidade |
| **order_items** (`olist_order_items_dataset.csv`) | Os itens comprados em cada pedido, com preço e frete | um item dentro de um pedido | orders, products, sellers | Valor vendido, frete, produtos e vendedores envolvidos em cada pedido |
| **payments** (`olist_order_payments_dataset.csv`) | Como cada pedido foi pago | uma forma de pagamento usada no pedido | orders | Valor pago, meio de pagamento e parcelamento |
| **order_reviews** (`olist_order_reviews_dataset.csv`) | A avaliação do cliente depois da compra | uma avaliação ligada a um pedido | orders | Satisfação (nota), comentários em texto e tempo de resposta da pesquisa |
| **products** (`olist_products_dataset.csv`) | O cadastro dos produtos vendidos | um produto | order_items, category_translation | Recortes por categoria, peso e tamanho (que pesam no frete) |
| **sellers** (`olist_sellers_dataset.csv`) | O cadastro dos vendedores (lojistas) parceiros | um vendedor | order_items, geolocation | Concentração de vendas e de atrasos por vendedor e por estado de origem |
| **geolocation** (`olist_geolocation_dataset.csv`) | Coordenadas de cada prefixo de CEP | um ponto de coordenada (o CEP se repete) | customers, sellers (por CEP) | Mapas e distância entre vendedor e cliente |
| *category_translation* (`product_category_name_translation.csv`) | Tradução das categorias para o inglês (apoio) | uma categoria | products | Padronizar os nomes das categorias em gráficos e relatórios |

### Colunas de cada tabela

**orders**: o pedido

| Coluna | Descrição |
|---|---|
| `order_id` | Identificador único do pedido (chave da tabela) |
| `customer_id` | Cliente do pedido; liga com `customers`. Cada pedido gera um `customer_id` novo |
| `order_status` | Situação do pedido: `delivered`, `shipped`, `canceled`, `unavailable`, `invoiced`, `processing`, `created`, `approved` |
| `order_purchase_timestamp` | Data e hora da compra |
| `order_approved_at` | Data e hora em que o pagamento foi aprovado |
| `order_delivered_carrier_date` | Data em que o vendedor entregou o pedido à transportadora (postagem) |
| `order_delivered_customer_date` | Data em que o cliente recebeu o pedido |
| `order_estimated_delivery_date` | Data de entrega prometida ao cliente na compra (sem hora) |

**customers**: o cliente

| Coluna | Descrição |
|---|---|
| `customer_id` | Identificador do cliente **naquele pedido** (chave da tabela; liga com `orders`) |
| `customer_unique_id` | Identificador da **pessoa**: é o mesmo em todas as compras do cliente. Use para contar clientes e recompra |
| `customer_zip_code_prefix` | 5 primeiros dígitos do CEP do cliente; liga com `geolocation` |
| `customer_city` | Cidade do cliente |
| `customer_state` | Estado (UF) do cliente |

**order_items**: os itens do pedido

| Coluna | Descrição |
|---|---|
| `order_id` | Pedido ao qual o item pertence; liga com `orders` |
| `order_item_id` | Número sequencial do item dentro do pedido (1, 2, 3…). Junto com `order_id`, forma a chave |
| `product_id` | Produto vendido; liga com `products` |
| `seller_id` | Vendedor do item; liga com `sellers` |
| `shipping_limit_date` | Prazo para o vendedor postar o item na transportadora |
| `price` | Preço do item (R$) |
| `freight_value` | Frete do item (R$). Se o pedido tem vários itens, o frete é dividido entre eles |

**payments**: o pagamento

| Coluna | Descrição |
|---|---|
| `order_id` | Pedido pago; liga com `orders` |
| `payment_sequential` | Número da forma de pagamento no pedido. Quem paga com mais de um meio, como cartão e voucher, gera várias linhas |
| `payment_type` | Meio de pagamento: `credit_card`, `boleto`, `voucher`, `debit_card`, `not_defined` |
| `payment_installments` | Número de parcelas |
| `payment_value` | Valor pago naquela forma de pagamento (R$) |

**order_reviews**: a avaliação

| Coluna | Descrição |
|---|---|
| `review_id` | Identificador da avaliação. Pode se repetir em pedidos diferentes |
| `order_id` | Pedido avaliado; liga com `orders` |
| `review_score` | Nota de 1 (pior) a 5 (melhor) |
| `review_comment_title` | Título do comentário, em português. Opcional, quase sempre vazio |
| `review_comment_message` | Texto do comentário, em português. Opcional; é o material para agentes que leem avaliações |
| `review_creation_date` | Data em que a pesquisa de satisfação foi enviada ao cliente |
| `review_answer_timestamp` | Data e hora em que o cliente respondeu |

**products**: o produto

| Coluna | Descrição |
|---|---|
| `product_id` | Identificador único do produto (chave da tabela) |
| `product_category_name` | Categoria em português; liga com `category_translation` |
| `product_name_lenght` | Quantidade de caracteres do nome do produto. O nome da coluna tem um erro de digitação no original (*lenght*) |
| `product_description_lenght` | Quantidade de caracteres da descrição do produto |
| `product_photos_qty` | Quantidade de fotos publicadas no anúncio |
| `product_weight_g` | Peso (gramas) |
| `product_length_cm` | Comprimento (cm) |
| `product_height_cm` | Altura (cm) |
| `product_width_cm` | Largura (cm) |

**sellers**: o vendedor

| Coluna | Descrição |
|---|---|
| `seller_id` | Identificador único do vendedor (chave da tabela) |
| `seller_zip_code_prefix` | 5 primeiros dígitos do CEP do vendedor; liga com `geolocation` |
| `seller_city` | Cidade do vendedor |
| `seller_state` | Estado (UF) do vendedor |

**geolocation**: a localização dos CEPs

| Coluna | Descrição |
|---|---|
| `geolocation_zip_code_prefix` | 5 primeiros dígitos do CEP. **Não é único**: o mesmo CEP tem vários pontos |
| `geolocation_lat` | Latitude |
| `geolocation_lng` | Longitude |
| `geolocation_city` | Cidade |
| `geolocation_state` | Estado (UF) |

**category_translation**: tradução das categorias, tabela de apoio

| Coluna | Descrição |
|---|---|
| `product_category_name` | Categoria em português (como em `products`) |
| `product_category_name_english` | Mesma categoria em inglês |

> As Etapas 1 e 2 conferem este dicionário nos dados: quantas linhas cada tabela tem, se a chave é mesmo única e se as ligações encontram par do outro lado.
