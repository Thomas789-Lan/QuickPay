# import qrcode
# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk

# def generate_qr():
#     upi_id = entry_upi.get()
#     name = entry_name.get()
#     amount = entry_amount.get()

#     if upi_id == "" or name == "":
#         messagebox.showwarning("Warning", "UPI ID and Name are required!")
#         return

#     # Create UPI link
#     if amount == "":
#         upi_link = f"upi://pay?pa={upi_id}&pn={name}&cu=INR"
#     else:
#         upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

#     # Generate QR
#     img = qrcode.make(upi_link)
#     img.save("payment_qr.png")

#     # Display QR
#     img = Image.open("payment_qr.png")
#     img = img.resize((220, 220))
#     img_tk = ImageTk.PhotoImage(img)

#     label_img.config(image=img_tk)
#     label_img.image = img_tk

#     messagebox.showinfo("Success", "QR Code Generated!")

# # Window setup
# root = tk.Tk()
# root.title("UPI QR Generator")
# root.geometry("350x450")

# # Title
# tk.Label(root, text="UPI QR Generator", font=("Arial", 16)).pack(pady=10)

# # UPI ID
# tk.Label(root, text="UPI ID").pack()
# entry_upi = tk.Entry(root, width=30)
# entry_upi.pack(pady=5)

# # Name
# tk.Label(root, text="Name").pack()
# entry_name = tk.Entry(root, width=30)
# entry_name.pack(pady=5)

# # Amount (optional)
# tk.Label(root, text="Amount (optional)").pack()
# entry_amount = tk.Entry(root, width=30)
# entry_amount.pack(pady=5)

# # Button
# btn = tk.Button(root, text="Generate QR", command=generate_qr)
# btn.pack(pady=15)

# # Image display
# label_img = tk.Label(root)
# label_img.pack(pady=10)

# root.mainloop()

# from flask import Flask, request, send_file, render_template_string
# import qrcode

# app = Flask(__name__)

# HTML = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>UPI QR Generator</title>
# </head>
# <body style="text-align:center; font-family:Arial;">
#     <h2>UPI QR Generator</h2>
    
#     <form method="POST">
#         <input name="upi" placeholder="UPI ID" required><br><br>
#         <input name="name" placeholder="Name" required><br><br>
#         <input name="amount" placeholder="Amount (optional)"><br><br>
#         <button type="submit">Generate QR</button>
#     </form>
    
#     {% if qr %}
#         <h3>Your QR Code:</h3>
#         <img src="/qr">
#     {% endif %}

#     <button onclick="shareQR()">Share QR</button>

#     <script>
#     function shareQR() {
#         const url = window.location.origin + "/qr";

#         if (navigator.share) {
#             navigator.share({
#                 title: "My UPI QR",
#                 text: "Scan to pay me",
#                 url: url
#             });
#         } else {
#             navigator.clipboard.writeText(url);
#             alert("Link copied! You can paste and share it.");
#         }
#     }
#     </script>
# </body>
# </html>
# """

# upi_link_global = ""

# @app.route("/", methods=["GET", "POST"])
# def home():
#     global upi_link_global
    
#     if request.method == "POST":
#         upi = request.form["upi"]
#         name = request.form["name"]
#         amount = request.form["amount"]

#         if amount == "":
#             upi_link_global = f"upi://pay?pa={upi}&pn={name}&cu=INR"
#         else:
#             upi_link_global = f"upi://pay?pa={upi}&pn={name}&am={amount}&cu=INR"

#         return render_template_string(HTML, qr=True)

#     return render_template_string(HTML, qr=False)


# @app.route("/qr")
# def qr():
#     img = qrcode.make(upi_link_global)
#     img.save("qr.png")
#     return send_file("qr.png", mimetype="image/png")


# app.run(debug=True)

from flask import Flask, request, send_file, render_template_string
import qrcode

app = Flask(__name__)

# 🔥 Your details (set once)
UPI_ID = "thlamuanpuii133@okhdfcbank"
NAME = "Lalthlamuanpuii"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Quick Pay</title>
    <link rel="manifest" href="/static/manifest.json">
    <link rel="icon" href="/static/icon.png">
    <style>
        body {
            font-family: Arial;
            text-align: center;
            background: #f5f5f5;
            padding: 50px;
        }
        .box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            width: 300px;
            margin: auto;
        }
        input, button {
            padding: 10px;
            margin: 10px;
            width: 80%;
        }
        button {
            background: black;
            color: white;
            border: none;
        }
    </style>
</head>
<body>

<div class="box">
    <h2>Pay Me</h2>

    <form method="POST">
        <input name="amount" placeholder="I thawn tur zat chu rawh." required>
        <button type="submit">Generate QR</button>
    </form>

    {% if qr %}
        <h3>Scan to Pay ₹{{amount}}</h3>
        <img src="/qr" width="200"><br><br>
        <a href="/qr" download="payment_qr.png">
            <button>Download</button>
        </a>
    {% endif %}
</div>

</body>
</html>
"""

upi_link_global = ""
amount_global = ""

@app.route("/", methods=["GET", "POST"])
def home():
    global upi_link_global, amount_global

    if request.method == "POST":
        amount = request.form["amount"]
        amount_global = amount

        upi_link_global = f"upi://pay?pa={UPI_ID}&pn={NAME}&am={amount}&cu=INR"

        return render_template_string(HTML, qr=True, amount=amount)

    return render_template_string(HTML, qr=False)


@app.route("/qr")
def qr():
    img = qrcode.make(upi_link_global)
    img.save("qr.png")
    return send_file("qr.png", mimetype="image/png")


app.run(host="0.0.0.0", port=5000)