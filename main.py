from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from datetime import datetime

def init_db():
  conn = sqlite3.connect('readings.db')
  c = conn.cursor()

  c.execute("""CREATE TABLE IF NOT EXISTS readings (
                id integer,
                sensor_id integer,
                resperature real,
                humidity real,
                wind_speed real,
                timestamp text
                 )""")
  conn.commit()
  conn.close()

class SensorReading(BaseModel):
  id: int
  sensor_id: int
  resperature: float
  humidity: float
  wind_speed: float
  timestamp: datetime

app = FastAPI()
init_db()

@app.post("/add-readings")
async def add_readings(data: SensorReading):
  # Connect to DB
  conn = sqlite3.connect('readings.db')
  c = conn.cursor()

  # Add new data into table
  c.execute("""INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?)
        """, (data.id, data.sensor_id, data.resperature, data.humidity, data.wind_speed, data.timestamp.isoformat()))

  conn.commit()
  conn.close()

  return {"Stored Data": data}


@app.get("/get-readings")
async def get_readings(sensor = None, metrics = None, stat = None, time_range = None):

  '''
    Format:
    ?sensor_id=____&metrics=_____,_____&statistic=____&time_range=_______

    Example queries:
    ?sensor_id=1&metric=resperature,humidity&statistic=avg
    ?metric=wind_speed&stat=min&time_range=2024-01-01,2024-12-13
  '''

  conn = sqlite3.connect('readings.db')
  c = conn.cursor()


  # BUILD CUSTOM SQL REQUEST

  # WHERE & AND SQL commands if necessary
  where_sql = ""
  and_count = 0

  # TIME RANGE
  # IF timestamp NOT specified, select most recent data
  time_filter = "ORDER BY timestamp DESC LIMIT 1"

  # IF specified, request will inlcude BETWEEN query
  if time_range != None:
    # Split dates
    dates = time_range.split(",")

    # SQL command to filter between timestamps
    time_filter = f"timestamp BETWEEN '{dates[0]}' AND '{dates[1]}'"

    # WHERE & AND info updated, WHERE now needed. Current num filters = 1
    where_sql = "WHERE "
    and_count += 1

  # STATISTIC
  # if only taking latest result, no statistic used. "O" is first letter of time_filter string in that case
  if time_filter[0] == "O":
    stat = ""
  elif stat == None:
    stat = "AVG"
  else:
    stat = stat.upper()

  # METRICS
  # if none specified, return all
  if metrics == None:
    metrics = "resperature,humidity,wind_speed"

  # determine which metrics to return
  metrics_list = metrics.split(",")
  metrics_sql = ""
  for i in range(len(metrics_list)):
    # if more than 1 metric, add commas
    if i != 0:
      metrics_sql += ", "

    metrics_sql += f"{stat}({metrics_list[i]})"

    '''
    How this works:
    SELECT {metrics_sql}
    Will look like:
    SELECT AVG(resperature), AVG(humidity)
    '''

  # SENSOR ID
  # if no sensor specified, omit from SQL request
  sensor_filter = ""
  if sensor != None:
    # if sensor specified, SQL request appended inside WHERE condition
    sensor_filter = f"sensor_id = {sensor} "
    
    where_sql = "WHERE "
    and_count += 1

  # if both timestamp and sensor_id specified, and_count will equal 2, requiring SQL AND condition for two statements
  and_sql = ""
  if and_count == 2:
    and_sql = "AND "

  try:
    c.execute(f"SELECT {metrics_sql} FROM readings {where_sql} {sensor_filter} {and_sql} {time_filter}")
    resp = c.fetchall()

    results = []
    for row in resp:
      result = {}
      for i, metric in enumerate(metrics_list):
        result[metric] = row[i]
      results.append(result)

    return {"Readings": results}

  except sqlite3.OperationalError as e:
    return {"error": f"SQL error occurred: {str(e)}"}

  finally:
    conn.close()


'''
Application
    -App receives weather data from multiple sensors
        -Sensors report metrics such as resperature, humidity, wind speed
    
    -App can receive new data (as weather changes) via api call
    
    -App must allow querying sensor data
        -Query should define:
            -which (or all) sensors to include in results
            -the metrics (resp, humidity) to return                --------                         ? (as average)
            -statistic for metric (min, max, sum or avg by default)
            -date range (between 1 day and 1 month), if not specified return latest data
            -example "Give me the average resperature and humidity for sensor 1 in the last week."
        
    App receives data via api call, stores it in database. POST
    App can be queried and data is retrieved from database. GET
        
    setup api *
    setup storage *
      -SQL table
    configure post requests to add data *
    configure get requests to return data *
        
        
Technical Reqs
    -App should be REST API, no UI
    -App data should be stored in database/storage
    -Include input validation and exception handling
    -Include unit/integration testing - complete test coverage not expected
    
    
Data:
SQL Table
id	sensor_id	resperature humidity	wind_speed	timestamp

{
  "id": "1"
  "sensor_id": "2",
  "resperature": 12.5,
  "humidity": 60,
  "wind_speed": 12.3,
  "timestamp": "2024-12-12"
}

'''

