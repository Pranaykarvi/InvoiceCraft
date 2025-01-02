from flask import Flask, render_template, request, jsonify, redirect, url_for
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    # Extract form data
    invoice_id = request.form.get('invoice_id')
    date = request.form.get('date')
    client_name = request.form.get('client_name')
    template = request.form.get('template', 'basic')  # Default to 'basic'
    items = []

    for i in range(int(request.form.get('item_count', 0))):
        items.append({
            'name': request.form.get(f'item_name_{i}'),
            'quantity': int(request.form.get(f'item_quantity_{i}', 0)),
            'price': float(request.form.get(f'item_price_{i}', 0)),
            'total': float(request.form.get(f'item_total_{i}', 0))
        })
    total_amount = sum(item['total'] for item in items)

    # Generate PDF based on template
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    if template == 'basic':
        pdf.cell(0, 10, f"Invoice ID: {invoice_id}", ln=1)
        pdf.cell(0, 10, f"Date: {date}", ln=1)
        pdf.cell(0, 10, f"Client Name: {client_name}", ln=1)
        pdf.ln(10)
    elif template == 'modern':
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "Modern Invoice", ln=1, align='C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"ID: {invoice_id} | Date: {date}", ln=1)
        pdf.cell(0, 10, f"Client: {client_name}", ln=1)
        pdf.ln(10)

    # Add item table
    for item in items:
        pdf.cell(100, 10, item['name'], border=1)
        pdf.cell(30, 10, str(item['quantity']), border=1)
        pdf.cell(30, 10, f"{item['price']:.2f}", border=1)
        pdf.cell(30, 10, f"{item['total']:.2f}", border=1, ln=1)

    pdf.ln(10)
    pdf.cell(0, 10, f"Total Amount: {total_amount:.2f}", ln=1)

    # Save PDF
    file_path = os.path.join(INVOICE_DIR, f"invoice_{invoice_id}.pdf")
    pdf.output(file_path)

    return jsonify({"message": "Invoice generated successfully.", "file_path": file_path})


if __name__ == '__main__':
    app.run(debug=True)

