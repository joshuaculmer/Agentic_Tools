# Json Structure

Make sure that all output is structured as valid json. In the event that there is something that you feel does not fit into any particular section of the json, make a new section titled other and add that information there. Instead of responding directly to the user, make sure that all responses are formatted as a valid json file

For example:
---------------------------
{
  "name": "Alice Johnson",
  "age": 28,
  "email": "alice@example.com",
  "isActive": true,
  "address": {
    "street": "123 Main St",
    "city": "Seattle",
    "state": "WA",
    "zipCode": "98101"
  },
  "hobbies": ["reading", "hiking", "photography"],
  "scores": [95, 87, 92, 88]
}

Another Example of valid json output would be:
----------------------------
{
  "location": {
    "name": "San Francisco",
    "region": "California",
    "country": "United States",
    "lat": 37.77,
    "lon": -122.42,
    "timezone": "America/Los_Angeles",
    "localtime": "2026-01-16 10:30"
  },
  "current": {
    "last_updated": "2026-01-16 10:00",
    "temp_c": 14.5,
    "temp_f": 58.1,
    "condition": {
      "text": "Partly cloudy",
      "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
      "code": 1003
    },
    "wind_mph": 8.1,
    "wind_kph": 13.0,
    "wind_degree": 270,
    "wind_dir": "W",
    "pressure_mb": 1013,
    "pressure_in": 29.92,
    "precip_mm": 0.0,
    "precip_in": 0.0,
    "humidity": 72,
    "cloud": 50,
    "feelslike_c": 13.2,
    "feelslike_f": 55.8,
    "vis_km": 16.0,
    "vis_miles": 9.0,
    "uv": 4,
    "gust_mph": 11.2,
    "gust_kph": 18.0
  },
  "forecast": {
    "forecastday": [
      {
        "date": "2026-01-16",
        "day": {
          "maxtemp_c": 16.8,
          "maxtemp_f": 62.2,
          "mintemp_c": 11.2,
          "mintemp_f": 52.2,
          "avgtemp_c": 14.0,
          "avgtemp_f": 57.2,
          "maxwind_mph": 10.5,
          "maxwind_kph": 16.9,
          "totalprecip_mm": 2.5,
          "totalprecip_in": 0.1,
          "avghumidity": 75,
          "condition": {
            "text": "Light rain",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/296.png",
            "code": 1183
          },
          "uv": 3
        },
        "hour": [
          {
            "time": "2026-01-16 00:00",
            "temp_c": 12.0,
            "temp_f": 53.6,
            "condition": {
              "text": "Clear",
              "code": 1000
            },
            "wind_kph": 8.6,
            "humidity": 78,
            "chance_of_rain": 0
          }
        ]
      }
    ]
  }
}

Here is a final example that you should follow most closely:
----------------------------