import csv

from app.db.crud import CRUDBase
from app.db.session import get_db

csv_file = "cleaned_data.csv"


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
        db.add(purchase_history)

# Commit the changes to the database


print("Dataset loaded successfully.")
