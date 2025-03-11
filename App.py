from flask import Flask, render_template_string, request, redirect, url_for
import requests

app = Flask(__name__)

def get_ip_info(ip_address):
    """Функция для запроса информации об IP"""
    url = f"http://ip-api.com/json/{ip_address}?fields=status,message,query,country,regionName,city,isp,lat,lon"
    response = requests.get(url).json()
    
    if response.get("status") != "success":
        return None
    
    return {
        "ip": response["query"],
        "city": response["city"],
        "region": response["regionName"],
        "country": response["country"],
        "isp": response["isp"],
        "lat": response["lat"],
        "lon": response["lon"]
    }

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CallRadar</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #1a1a1a;
                color: white;
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            h1 {
                font-size: 48px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 20px;
                text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8);
            }
            p {
                font-size: 20px;
                text-align: center;
                margin: 10px 0;
                max-width: 800px;
                color: #ccc;
                line-height: 1.5;
            }
            .container {
                background-color: #333;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.8);
                width: 90%;
                max-width: 1000px;
                text-align: center;
            }
            .button {
                background-color: #ff5722;
                color: white;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 25px;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
                transition: background-color 0.3s, transform 0.3s;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            }
            .button:hover {
                background-color: #e64a19;
                transform: translateY(-5px);
            }
            .button:active {
                background-color: #d84315;
                transform: translateY(2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Приветствуем в CallRadar</h1>
            <p>Это проект для поиска дополнительной информации по номеру, ФИО, и т.д.</p>
            <a href="{{ url_for('search_ip') }}" class="button">Пробить по IP</a>
        </div>
    </body>
    </html>
    """)

@app.route("/search_ip", methods=["GET", "POST"])
def search_ip():
    ip_info = None
    error = None

    if request.method == "POST":
        ip_address = request.form.get("ip_address", "").strip()
        
        if not ip_address:
            error = "Введите IP-адрес!"
        else:
            ip_info = get_ip_info(ip_address)
            if not ip_info:
                error = "Не удалось получить данные для этого IP."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Поиск по IP</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #1a1a1a;
                color: white;
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            h1 {
                font-size: 48px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 20px;
                text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8);
            }
            p {
                font-size: 20px;
                text-align: center;
                margin: 10px 0;
                max-width: 800px;
                color: #ccc;
                line-height: 1.5;
            }
            .container {
                background-color: #333;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.8);
                width: 90%;
                max-width: 1000px;
                text-align: center;
            }
            .button {
                background-color: #ff5722;
                color: white;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 25px;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
                transition: background-color 0.3s, transform 0.3s;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            }
            .button:hover {
                background-color: #e64a19;
                transform: translateY(-5px);
            }
            .button:active {
                background-color: #d84315;
                transform: translateY(2px);
            }
            .input-container {
                margin-top: 20px;
            }
            input {
                padding: 10px;
                font-size: 18px;
                border-radius: 5px;
                border: 1px solid #555;
                width: 100%;
                max-width: 400px;
            }
            .submit-button {
                background-color: #4caf50;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                margin-top: 10px;
                width: 100%;
                max-width: 400px;
            }
            .submit-button:hover {
                background-color: #45a049;
            }
            .result {
                background-color: #222;
                margin-top: 30px;
                padding: 15px;
                border-radius: 8px;
                text-align: left;
                width: 100%;
                max-width: 600px;
            }
            .error {
                color: #ff0000;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Поиск по IP</h1>
            <p>Введите IP-адрес для получения информации:</p>

            <div class="input-container">
                <form method="POST">
                    <input type="text" name="ip_address" placeholder="Введите IP-адрес" required>
                    <button type="submit" class="submit-button">Выдать результат</button>
                </form>
            </div>

            {% if error %}
                <div class="error">{{ error }}</div>
            {% elif ip_info %}
                <div class="result">
                    <p><b>IP:</b> {{ ip_info.ip }}</p>
                    <p><b>Город:</b> {{ ip_info.city }}</p>
                    <p><b>Регион:</b> {{ ip_info.region }}</p>
                    <p><b>Страна:</b> {{ ip_info.country }}</p>
                    <p><b>Провайдер:</b> {{ ip_info.isp }}</p>
                    <p><b>Координаты:</b> {{ ip_info.lat }}, {{ ip_info.lon }}</p>
                    <a href="https://www.google.com/maps?q={{ ip_info.lat }},{{ ip_info.lon }}" target="_blank" class="button">Показать на карте</a>
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """ , ip_info=ip_info, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
