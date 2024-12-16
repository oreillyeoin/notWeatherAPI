### Dependencies

_FastAPI_: Web framework for building APIs in Python  
_Uvicorn_: Web server implementation for Python  
_pytest_: Testing framework for Python  
_HTTPX_: HTTP client for Python  
_(pip install fastapi uvicorn pytest httpx)_
 
### Running the API
  
Uvicorn used to run the script in the command line _(uvicorn main:app --reload)_.   
Postman used for GET and POST requests _(https://www.postman.com/)_. 


### GET REQUESTS 
_(127.0.0.1:8000/get-readings)_
##### Query Format: 
/get-readings?sensor=XXXX&metrics=XXXX,XXXX&stat=XXXX&time_range=XXXX,XXXX
##### Example queries:  
/get-readings?sensor=1&metrics=temperature,humidity&stat=avg  
/get-readings?metrics=wind_speed&stat=min&time_range=2024-01-01,2024-12-13  
/get-readings?sensor=3&metrics=humidity&stat=sum&time_range=2024-01-01,2025,01-01  

### POST REQUESTS 
_(127.0.0.1:8000/add-reading)_
##### Data Format:
```
{  
  "id": "2321",  
  "sensor_id": "2",  
  "temperature": 12.5,  
  "humidity": 60,  
  "wind_speed": 12.3,  
  "timestamp": "2024-12-12"  
}  
```
