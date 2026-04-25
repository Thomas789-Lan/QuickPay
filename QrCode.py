from flask import Flask, request, render_template_string, redirect, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

upi_link_global = ""
amount_global = ""
name_global = ""

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QuickPay</title>
    <link rel="icon" href="icon.png">
    <meta name="google-site-verification" content="googlef420cb4077c9e78d.html" />
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .card {
            background: white;
            width: 340px;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        .amount {
            font-size: 40px;
            font-weight: bold;
            margin: 10px 0;
        }

        .name {
            color: #666;
            margin-bottom: 20px;
        }

        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 12px;
            border: 1px solid #ddd;
        }

        button {
            width: 100%;
            padding: 13px;
            border-radius: 12px;
            border: none;
            background: #1a73e8;
            color: white;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }

        .secondary {
            background: #ccc;
            color: black;
        }

        img {
            margin-top: 15px;
            border-radius: 10px;
        }

        .note {
            font-size: 12px;
            color: gray;
        }
    </style>

    <script>
        if (window.location.pathname === "/show") {
            window.onbeforeunload = function() {
                window.location.href = "/";
            };
        }
    </script>

</head>

<body>

<div class="card">

    <form method="POST">
        <input name="upi" placeholder="Enter UPI ID" required>
        <input name="name" placeholder="Enter Name" required>
        <input name="amount" placeholder="Enter Amount ₹" required>
        <button type="submit">Generate QR</button>
    </form>

    {% if qr %}
        <div class="amount">₹{{amount}}</div>
        <div class="name">to {{name}}</div>

        <img src="/qr" width="200">

        <div class="note">Scan using any UPI app</div>

        <a href="/">
            <button class="secondary">New Payment</button>
        </a>
    {% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    global upi_link_global, amount_global, name_global

    if request.method == "POST":
        upi = request.form["upi"]
        name = request.form["name"]
        amount = request.form["amount"]

        upi_link_global = f"upi://pay?pa={upi}&pn={name}&am={amount}&cu=INR"
        amount_global = amount
        name_global = name

        return redirect("/show")

    return render_template_string(HTML, qr=False)


@app.route("/show")
def show():
    return render_template_string(
        HTML,
        qr=True,
        amount=amount_global,
        name=name_global
    )


@app.route("/qr")
def qr():
    img = qrcode.make(upi_link_global)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
