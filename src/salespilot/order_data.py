"""订单数据。供 seed.py 灌入 orders 表。"""

# 每个订单是一个字典。status 取值：
#   pending(待付款) / paid(已付款) / shipped(已发货) / completed(已完成)
ORDERS = [
    {
        "order_no": "ORD20260917001",
        "user_id": 1001,
        "product_id": 1,
        "quantity": 1,
        "total_price": 299.0,
        "status": "pending",
    },
    {
        "order_no": "ORD20260917002",
        "user_id": 1001,
        "product_id": 2,
        "quantity": 2,
        "total_price": 918.0,
        "status": "paid",
    },
    {
        "order_no": "ORD20260917003",
        "user_id": 1002,
        "product_id": 3,
        "quantity": 1,
        "total_price": 89.0,
        "status": "shipped",
    },
    {
        "order_no": "ORD20260917004",
        "user_id": 1002,
        "product_id": 4,
        "quantity": 1,
        "total_price": 199.0,
        "status": "completed",
    },
]