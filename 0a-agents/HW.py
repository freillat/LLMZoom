import random

known_weather_data = {
    'berlin': 20.0
}

def get_weather(city: str) -> float:
    city = city.strip().lower()

    if city in known_weather_data:
        return known_weather_data[city]

    return round(random.uniform(-5, 35), 1)

get_weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Retrieves current weather data for a specified city. If the city is not 'berlin', it generates fake weather data.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city for which to get weather data (e.g., 'London', 'Paris', 'Berlin')"
            }
        },
        "required": ["city"],
        "additionalProperties": False
    }
}

def set_weather(city: str, temp: float) -> None:
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'

set_weather_tool = {
    "type": "function",
    "name": "set_weather",
    "description": "Sets or updates the current weather data for a specified city in the database.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city for which to set the weather data (e.g., 'London', 'Paris', 'Berlin')"
            },
            "temp": {
                "type": "number", # Use "number" for floats
                "description": "The temperature to set for the city (e.g., 25.5, -3.0)"
            }
        },
        "required": ["city", "temp"],
        "additionalProperties": False
    }
}