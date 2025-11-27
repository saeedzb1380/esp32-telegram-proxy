from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🚀 ESP32 Telegram Proxy</h1>
    <p>Server is running on Render!</p>
    <p>Use POST to /send endpoint</p>
    '''

@app.route('/test')
def test():
    return jsonify({'status': 'active', 'message': 'Render Server is working!'})

@app.route('/send', methods=['POST'])
def send_message():
    try:
        # دریافت داده از ESP32
        data = request.get_json()
        
        print(f"📨 Received data: {data}")
        
        # بررسی فیلدهای ضروری
        if not data or 'bot_token' not in data or 'chat_id' not in data or 'text' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        bot_token = data['bot_token']
        chat_id = data['chat_id']
        text = data['text']
        
        print(f"🤖 Sending to Telegram: {text}")
        
        # ارسال به تلگرام - در Render مشکلی نداره
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        
        # ارسال درخواست به تلگرام
        response = requests.post(telegram_url, json=payload, timeout=10)
        
        print(f"📡 Telegram response: {response.status_code}")
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Message sent to Telegram! 🎉'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Telegram API error: {response.status_code}',
                'details': response.text
            })
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
