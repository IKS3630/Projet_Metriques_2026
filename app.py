import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :

@app.route("/contact")
def MaPremiereAPI():
    return render_template("contact.html")

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphiques.html")


@app.route("/histogramme")
def mon_histogramme():
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522"
        "&daily=temperature_2m_max&timezone=Europe/Paris&forecast_days=7"
    )
    response = requests.get(url)
    data = response.json()

    labels = data.get("daily", {}).get("time", [])
    temps = data.get("daily", {}).get("temperature_2m_max", [])

    return render_template("histogramme.html", labels=labels, temps=temps)


@app.route("/atelier")
def mon_atelier():
    # Liste de villes proposées (majoritairement en Asie)
    # Conserver Tokyo et Beijing (Asie) et ajouter 2 villes par continent
    cities = {
        # Asie
        'Tokyo': (35.6895, 139.6917),
        'Beijing': (39.9042, 116.4074),
        # Europe
        'Paris': (48.8566, 2.3522),
        'Rome': (41.9028, 12.4964),
        # Amérique du Sud
        'Sao Paulo': (-23.5505, -46.6333),
        'Buenos Aires': (-34.6037, -58.3816),
        # Afrique
        'Nairobi': (-1.2921, 36.8219),
        'Johannesburg': (-26.2041, 28.0473),
    }

    selected = request.args.get('city', 'Tokyo')
    latitude, longitude = cities.get(selected, cities['Tokyo'])

    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
        "&daily=temperature_2m_max&forecast_days=7&timezone=auto"
    )
    response = requests.get(url)
    data = response.json()

    labels = data.get("daily", {}).get("time", [])
    temps = data.get("daily", {}).get("temperature_2m_max", [])

    # Calculer un indicateur simple : température moyenne et score de chaleur (0-100)
    avg_temp = None
    heat_score = None
    if temps:
        try:
            avg_temp = round(sum(temps) / len(temps), 1)
            # Normaliser :  -10°C -> 0 ; 40°C -> 100
            heat_score = int(max(0, min(100, (avg_temp + 10) / 50 * 100)))
        except Exception:
            avg_temp = None
            heat_score = None

    return render_template(
        "atelier.html",
        labels=labels,
        temps=temps,
        avg_temp=avg_temp,
        heat_score=heat_score,
        cities=list(cities.keys()),
        selected_city=selected,
    )


# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
