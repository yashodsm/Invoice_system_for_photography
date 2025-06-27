import sqlite3
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from datetime import date

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure Flask-Mail (Update these with your actual email credentials)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='someone@gmail.com',  # Your email
    MAIL_PASSWORD='somepassword',          # Use app password or secure method
)

mail = Mail(app)

DB_PATH = 'invoices.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            email TEXT NOT NULL,
            line_items TEXT NOT NULL,
            event_date TEXT,
            link TEXT,
            invoice_number TEXT,
            invoice_date TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            tax_rate REAL DEFAULT 10.0
        )
        ''')
        conn.commit()

@app.route('/')
def home():
    conn = get_db_connection()
    invoices = conn.execute('SELECT * FROM invoices ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('home.html', invoices=invoices)

@app.route('/invoice/create', methods=['GET', 'POST'])
@app.route('/invoice/edit/<int:id>', methods=['GET', 'POST'])
def create_edit(id=None):
    conn = get_db_connection()
    invoice = None
    line_items = []

    if id:
        invoice = conn.execute('SELECT * FROM invoices WHERE id=?', (id,)).fetchone()
        if invoice:
            line_items = json.loads(invoice['line_items'])

    if request.method == 'POST':
        client_name = request.form['client_name']
        email = request.form['email']
        invoice_number = request.form.get('invoice_number', '')
        invoice_date = request.form.get('invoice_date', '')
        due_date = request.form.get('due_date', '')
        event_date = request.form.get('event_date', '')
        link = request.form.get('link', '')
        tax_rate = float(request.form.get('tax_rate', 10))

        descriptions = request.form.getlist('description[]')
        quantities = request.form.getlist('quantity[]')
        prices = request.form.getlist('price[]')

        # Validate line items and build JSON
        items = []
        for d, q, p in zip(descriptions, quantities, prices):
            if d.strip() == '':
                continue
            try:
                item = {
                    'description': d.strip(),
                    'quantity': int(q),
                    'price': float(p)
                }
                items.append(item)
            except:
                flash("Invalid quantity or price input", "danger")
                return redirect(request.url)

        line_items_json = json.dumps(items)

        if id:
            conn.execute('''
                UPDATE invoices SET client_name=?, email=?, line_items=?, event_date=?, link=?, invoice_number=?, 
                invoice_date=?, due_date=?, tax_rate=? WHERE id=?
            ''', (client_name, email, line_items_json, event_date, link, invoice_number, invoice_date, due_date, tax_rate, id))
            conn.commit()
            flash("Invoice updated successfully.", "success")
        else:
            conn.execute('''
                INSERT INTO invoices (client_name, email, line_items, event_date, link, invoice_number, invoice_date, due_date, tax_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (client_name, email, line_items_json, event_date, link, invoice_number, invoice_date, due_date, tax_rate))
            conn.commit()
            flash("Invoice created successfully.", "success")

        conn.close()
        return redirect(url_for('home'))

    conn.close()
    return render_template('create_edit.html', invoice=invoice, line_items=line_items, today_date=date.today().isoformat())

@app.route('/invoice/email/<int:id>')
def email_invoice(id):
    conn = get_db_connection()
    invoice = conn.execute('SELECT * FROM invoices WHERE id=?', (id,)).fetchone()
    conn.close()
    if not invoice:
        flash("Invoice not found.", "danger")
        return redirect(url_for('home'))

    line_items = json.loads(invoice['line_items'])
    subtotal = sum(item['quantity'] * item['price'] for item in line_items)
    tax_amount = subtotal * (invoice['tax_rate'] / 100)
    total = subtotal + tax_amount

    # Build email content
    lines_html = "".join(
        f"<tr><td>{item['description']}</td><td>{item['quantity']}</td><td>${item['price']:.2f}</td><td>${item['quantity']*item['price']:.2f}</td></tr>"
        for item in line_items
    )
    html = f"""
    <h2>Invoice #{invoice['invoice_number']}</h2>
    <p><strong>Client:</strong> {invoice['client_name']}<br>
    <strong>Email:</strong> {invoice['email']}<br>
    <strong>Invoice Date:</strong> {invoice['invoice_date']}<br>
    <strong>Due Date:</strong> {invoice['due_date']}</p>

    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
    <thead>
        <tr><th>Description</th><th>Quantity</th><th>Price</th><th>Total</th></tr>
    </thead>
    <tbody>
        {lines_html}
    </tbody>
    </table>

    <p><strong>Subtotal:</strong> ${subtotal:.2f}<br>
    <strong>Tax ({invoice['tax_rate']}%):</strong> ${tax_amount:.2f}<br>
    <strong>Total:</strong> ${total:.2f}</p>

    <p>Event Date(s): {invoice['event_date']}</p>
    <p>Album/Link: <a href="{invoice['link']}" target="_blank">{invoice['link']}</a></p>
    """

    try:
        msg = Message(subject=f"Invoice #{invoice['invoice_number']} from ClickThatPhotography",
                      recipients=[invoice['email']],
                      html=html,
                      sender=app.config['MAIL_USERNAME'])
        mail.send(msg)
        flash("Invoice emailed successfully.", "success")
    except Exception as e:
        flash(f"Failed to send email: {e}", "danger")

    return redirect(url_for('home'))

@app.route('/invoice/delete/<int:id>', methods=['POST'])
def delete_invoice(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM invoices WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash("Invoice deleted.", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
