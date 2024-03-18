import csv

from app.db.crud import CRUDBase
from app.db.session import get_db
from app.models.dataset import Dataset

csv_file = "cleaned_data.csv"

dataset_crud = CRUDBase(model=Dataset)

get_db_session = get_db()

with open(csv_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        purchase_history = PurchaseHistory(
            invoice_id=row["InvoiceNo"],
            stock_code=row["StockCode"],
            description=row["Description"],
            quantity=int(row["Quantity"]),
            invoice_date=row["InvoiceDate"],
            unit_price=float(row["UnitPrice"]),
            customer_id=int(row["CustomerID"]),
            country=row["Country"]
        )
        dataset_crud.create(db=get_db_session, obj_in=purchase_history)



print("Dataset loaded successfully.")
