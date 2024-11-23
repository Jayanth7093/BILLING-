from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)

items = {
    'rice': 60,
    'sugar': 40,
    'oil': 100,
    'chilli powder': 50,
    'turmeric powder': 80,
    'paneer': 110,
    'maggie': 50,
    'salt': 20,
    'garam masala': 50,
    'chicken masala': 100,
    'colgate': 85
}

@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/bill', methods=['POST'])
def bill():
    name = request.form['name']
    email = request.form['email']
    chosen_items = request.form.getlist('items')
    quantities = request.form.getlist('quantities')
    choice = request.form['choice']

    total_price = 0
    item_list = []
    quantity_list = []
    price_list = []

    for item, quantity in zip(chosen_items, quantities):
        quantity = float(quantity)
        price = quantity * items[item]
        item_list.append(item)
        quantity_list.append(quantity)
        price_list.append(price)
        total_price += price

    gst = (total_price * 5) / 100
    final_amount = total_price + gst

    bill_content = f"""
    <html>
    <body>
        <h2>Jayanth Stores</h2>
        <p>Tirupati</p>
        <p>Name: {name} <span style="float:right">Date: {datetime.now()}</span></p>
        <hr>
        <table border="1" style="width:100%; border-collapse: collapse;">
            <tr>
                <th>S.No</th>
                <th>Items</th>
                <th>Quantity</th>
                <th>Price</th>
            </tr>
    """
    
    for i in range(len(item_list)):
        bill_content += f"""
            <tr>
                <td>{i + 1}</td>
                <td>{item_list[i]}</td>
                <td>{quantity_list[i]} kg</td>
                <td>{price_list[i]}</td>
            </tr>
        """
    
    bill_content += f"""
        </table>
        <hr>
        <p>Total Amount: Rs {total_price}</p>
        <p>GST Amount: Rs {gst}</p>
        <hr>
        <p>Final Amount: Rs {final_amount}</p>
        <hr>
        <p>Thanks for Visiting</p>
    </body>
    </html>
    """

    if choice == 'email':
        def send_email(subject, body, to_email):
            from_email = "2021csd.r31@svce.edu.in"
            from_password = "Jayanth1683012@1"  # Use an app-specific password if you have 2FA

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()

        send_email("Your Bill from Jayanth Stores", bill_content, email)
        return "Bill sent to your email successfully!"
    
    return render_template('bill.html', bill_content=bill_content)

if __name__ == "__main__":
    app.run(debug=True)