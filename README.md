# notWeatherAPI
This is definitely not a weather API

Dependencies:
FastAPI: Web framework for building APIs in Python (pip install fastapi)
Uvicorn: Web server implementation for Python (pip install uvicorn)

Running the API:
Uvicorn used to run the script in the command line (uvicorn main:app --reload).
Postman used for GET and POST requests (https://www.postman.com/)

GET REQUESTS
(127.0.0.1:8000/get-readings)
Query Format:
/get-readings?sensor_id=____&metrics=_____,_____&statistic=____&time_range=____,____

Example queries:
?sensor_id=1&metrics=temperature,humidity&statistic=avg
?metrics=wind_speed&stat=min&time_range=2024-01-01,2024-12-13



POST REQUESTS
(127.0.0.1:8000/add-reading)
Reading Format:
{
  "id": "1",
  "sensor_id": "2",
  "temperature": 12.5,
  "humidity": 60,
  "wind_speed": 12.3,
  "timestamp": "2024-12-12"
}

TBC
