import requests

# API URL
url = "http://127.0.0.1:5000/generate_invoice"

# Sample Data
data = {
    "invoice_id": "12345",
    "date": "2025-01-01",
    "client_name": "PRANAY KARVI",
    "items": [
        {"name": "Laptop", "quantity": 2, "price": 1000.0, "total": 2000.0},
        {"name": "Mouse", "quantity": 2, "price": 25.0, "total": 50.0}
    ],
    "total_amount": 2050.0
}

# Send POST request
response = requests.post(url, json=data)

# Print Response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
