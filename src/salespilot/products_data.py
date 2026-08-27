"""商品数据。先用内存里的列表模拟"数据库"，Phase 4 再升级为 PostgreSQL。"""

# 每个商品是一个字典：id/名称/价格/库存/分类/描述
PRODUCTS = [
    {
        "id": 1,
        "name": "静音机械键盘 87键",
        "price": 299.0,
        "stock": 120,
        "category": "键盘",
        "description": "红轴静音，适合办公室使用",
    },
    {
        "id": 2,
        "name": "无线蓝牙耳机 Pro",
        "price": 459.0,
        "stock": 8,
        "category": "耳机",
        "description": "主动降噪，续航30小时",
    },
    {
        "id": 3,
        "name": "办公鼠标 静音款",
        "price": 89.0,
        "stock": 200,
        "category": "鼠标",
        "description": "静音按键，人体工学",
    },
    {
        "id": 4,
        "name": "便携蓝牙音箱",
        "price": 199.0,
        "stock": 0,
        "category": "音箱",
        "description": "防水防尘，户外可用",
    },
]
