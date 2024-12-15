Dependencies:  
FastAPI: Web framework for building APIs in Python  
Uvicorn: Web server implementation for Python  
pytest: Testing framework for Python  
HTTPX: HTTP client for Python  
(pip install fastapi uvicorn pytest httpx)   
 
Running the API:  
Uvicorn used to run the script in the command line (uvicorn main:app --reload).   
Postman used for GET and POST requests (https://www.postman.com/)  

GET REQUESTS (127.0.0.1:8000/get-readings)  
Query Format: /get-readings?sensor=XXXXX&metrics=XXXXX,XXXXX&stat=XXXXX&time_range=XXXXX,XXXXX
Example queries:  
/get-readings?sensor=1&metrics=temperature,humidity&stat=avg  
/get-readings?metrics=wind_speed&stat=min&time_range=2024-01-01,2024-12-13  
/get-readings?sensor=3&metrics=humidity&stat=sum&time_range=2024-01-01,2025,01-01  

POST REQUESTS (127.0.0.1:8000/add-reading)  
Data Format:
{
  "id": "2321",
  "sensor_id": "2",
  "temperature": 12.5,
  "humidity": 60,
  "wind_speed": 12.3,
  "timestamp": "2024-12-12"
}
