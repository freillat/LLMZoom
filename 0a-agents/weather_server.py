# weather_server.py
import random
from fastmcp import FastMCP

# Global known_weather_data
known_weather_data = {
    'berlin': 20.0
}

mcp = FastMCP("Demo 🚀")

@mcp.tool
def get_weather(city: str) -> float:
    """
    Retrieves the temperature for a specified city.
    Parameters:
        city (str): The name of the city for which to retrieve weather data.
    Returns:
        float: The temperature associated with the city.
    """
    city = city.strip().lower()

    if city in known_weather_data:
        return known_weather_data[city]

    return round(random.uniform(-5, 35), 1)

@mcp.tool
def set_weather(city: str, temp: float) -> None:
    """
    Sets the temperature for a specified city.
    Parameters:
        city (str): The name of the city for which to set the weather data.
        temp (float): The temperature to associate with the city.
    Returns:
        str: A confirmation string 'OK' indicating successful update.
    """
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'

if __name__ == "__main__":
    mcp.run()

# LIST

# {"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"get_weather","description":"Retrieves the temperature for a specified city.\nParameters:\n    city (str): The name of the city for which to retrieve weather data.\nReturns:\n    float: The temperature associated with the city.","inputSchema":{"properties":{"city":{"title":"City","type":"string"}},"required":["city"],"type":"object"},"outputSchema":{"properties":{"result":{"title":"Result","type":"number"}},"required":["result"],"title":"_WrappedResult","type":"object","x-fastmcp-wrap-result":true}},{"name":"set_weather","description":"Sets the temperature for a specified city.\nParameters:\n    city (str): The name of the city for which to set the weather data.\n    temp (float): The temperature to associate with the city.\nReturns:\n    str: A confirmation string 'OK' indicating successful update.","inputSchema":{"properties":{"city":{"title":"City","type":"string"},"temp":{"title":"Temp","type":"number"}},"required":["city","temp"],"type":"object"}}]}}

# QUESTION 5
# {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_weather", "arguments": { "city": "Berlin"}}}