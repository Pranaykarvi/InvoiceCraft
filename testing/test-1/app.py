# InvoiceCraft: A Comprehensive Invoice Generator API

from flask import Flask, request, jsonify
from fpdf import FPDF
import os

app = Flask(__name__)

# Directory to save invoices
INVOICE_DIR = r"D:\target\full_stack\Invoice_Craft\invoices"
if not os.path.exists(INVOICE_DIR):
    os.makedirs(INVOICE_DIR)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Invoice', border=0, ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    data = request.json

    # Validate required fields
    required_fields = ['invoice_id', 'date', 'client_name', 'items', 'total_amount']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required."}), 400

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Invoice header
    pdf.cell(0, 10, f"Invoice ID: {data['invoice_id']}", ln=1)
    pdf.cell(0, 10, f"Date: {data['date']}", ln=1)
    pdf.cell(0, 10, f"Client Name: {data['client_name']}", ln=1)

    # Invoice items
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 10, 'Item', border=1)
    pdf.cell(30, 10, 'Quantity', border=1)
    pdf.cell(30, 10, 'Price', border=1)
    pdf.cell(30, 10, 'Total', border=1, ln=1)

    pdf.set_font('Arial', '', 12)
    for item in data['items']:
        pdf.cell(100, 10, item['name'], border=1)
        pdf.cell(30, 10, str(item['quantity']), border=1)
        pdf.cell(30, 10, f"{item['price']:.2f}", border=1)
        pdf.cell(30, 10, f"{item['total']:.2f}", border=1, ln=1)

    # Total amount
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Total Amount: {data['total_amount']:.2f}", ln=1)

    # Save PDF
    file_path = os.path.join(INVOICE_DIR, f"invoice_{data['invoice_id']}.pdf")
    pdf.output(file_path)

    return jsonify({"message": "Invoice generated successfully.", "file_path": file_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
