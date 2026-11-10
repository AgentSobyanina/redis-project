import pandas as pd
import redis

table = pd.read_excel("data.xlsx")

name_column = "Наименование управляющей организации, жилищного объединения"
orders_column = "Выдано предписаний"
fine_column = "Сумма штрафа (тыс. руб.)"

selected = table.loc[
    table[orders_column] > 10,
    [name_column, orders_column, fine_column],
]

db = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

for number, (name, orders, fine) in enumerate(
    selected.itertuples(index=False, name=None), start=1
):
    db.hset(f"organization:{number}", mapping={
        "Организация": name,
        "Выдано предписаний": orders,
        "Сумма штрафов, тыс. руб.": fine,
    })

print(db.hgetall("organization:1"))
count = sum(1 for _ in db.scan_iter(match="organization:*"))
print(f"Количество хэш-таблиц: {count}")