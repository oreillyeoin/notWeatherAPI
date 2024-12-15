# notWeatherAPI
This is definitely not a weather API

Dependencies:  
FastAPI: Web framework for building APIs in Python  
Uvicorn: Web server implementation for Python  
pytest: Testing framework for Python - for integration tests  
HTTPX: HTTP client for Python  
(pip install fastapi uvicorn pytest httpx)  

Running the API:
Uvicorn used to run the script in the command line (uvicorn main:app --reload).
Postman used for GET and POST requests (https://www.postman.com/)

GET REQUESTS (127.0.0.1:8000/get-readings)
Query Format:
/get-readings?sensor=____&metrics=_____,_____&stat=____&time_range=____,____

Example queries:
?sensor=1&metrics=temperature,humidity&stat=avg

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
