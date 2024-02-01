import requests
from flask import current_app

# Словарь с переводами состояний погоды
weather_translations = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "heavy-rain": "сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "thunderstorm-with-hail": "гроза с градом"
}


def translate_weather_condition(condition):
    """ Функция, отвечающая за перевод состояния погоды с английского на русский """
    return weather_translations.get(condition, condition)


def get_weather():
    """ Функция, отвечающая за получение данных с сервиса погоды """
    base_url = current_app.config['WEATHER_URL']
    headers = {
        "X-Yandex-API-Key": current_app.config['WEATHER_API_KEY']
    }

    params = {
        "lat": current_app.config['LATITUDE'],
        "lon": current_app.config['LONGITUDE'],
        "extra": "true",
        "lang": "ru_RU"
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        today_forecast = weather_data["forecasts"][0]["parts"]["day"]
        tomorrow_forecast = weather_data["forecasts"][1]["parts"]["day"]
        weekend_forecast = weather_data["forecasts"][2]["parts"]["day"]
        return today_forecast, tomorrow_forecast, weekend_forecast
    else:
        print(f"Ошибка при получении данных о погоде. Код ошибки: {response.status_code}")


if __name__ == "__main__":
    get_weather()
