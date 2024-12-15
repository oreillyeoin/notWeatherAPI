from fastapi import FastAPI, HTTPException, Request
import sqlite3
from pydantic import BaseModel
from datetime import datetime

# Method to create SQL table and insert data
def init_db():
    conn = sqlite3.connect('readings.db')
    c = conn.cursor()

    # check if readings table already exists
    c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='readings';")
    table_exists = c.fetchone()

    # if does not, create table and fill with data
    if not table_exists:
        c.execute("""CREATE TABLE readings (
                  id integer,
                  sensor_id integer,
                  temperature real,
                  humidity real,
                  wind_speed real,
                  timestamp text
                   )""")

        readings = [
            (3435, 1, 22.5, 55.0, 10.2, "2024-12-10 08:00:00"),
            (7823, 1, 23.1, 56.3, 9.8, "2024-12-10 10:00:00"),
            (1298, 1, 24.2, 58.1, 12.0, "2024-12-10 12:00:00"),
            (6754, 1, 25.0, 60.0, 8.5, "2024-12-10 14:00:00"),
            (9184, 2, 19.8, 65.0, 15.0, "2024-12-11 09:00:00"),
            (4672, 2, 20.3, 63.5, 13.5, "2024-12-11 11:00:00"),
            (3301, 2, 18.6, 67.2, 14.8, "2024-12-11 13:00:00"),
            (2947, 2, 21.0, 64.5, 12.5, "2024-12-11 15:00:00"),
            (5032, 3, 21.3, 70.2, 8.5, "2024-12-12 07:30:00"),
            (1148, 3, 22.8, 68.0, 10.0, "2024-12-12 09:30:00"),
            (7296, 3, 20.0, 72.1, 9.5, "2024-12-12 11:30:00"),
            (8624, 3, 23.5, 66.8, 11.3, "2024-12-12 13:30:00")
        ]

        c.executemany("INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?)", readings)

    conn.commit()
    conn.close()


# Class for holding Weather Reading data
# BaseModel enables automatic input validation, error message with invalid or missing fields will be returned
class Reading(BaseModel):
    id: int
    sensor_id: int
    temperature: float
    humidity: float
    wind_speed: float
    timestamp: datetime


# init code
app = FastAPI()
init_db()


# Method to handle POST requests, for receiving weather updates
@app.post("/add-reading")
async def add_reading(data: Reading):
    # Connect to DB
    conn = sqlite3.connect('readings.db')
    c = conn.cursor()

    # check for duplicate updates
    c.execute("SELECT 1 FROM readings WHERE id = ?", (data.id,))
    if c.fetchone():
        return {"error": "Reading ID already exists"}

    # Add new reading into table
    c.execute("INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?)",
              (data.id, data.sensor_id, data.temperature, data.humidity, data.wind_speed, data.timestamp))

    conn.commit()
    conn.close()

    return {"Reading Stored Successfully": data}


# Method for handling GET requests, accessing and returning weather data
@app.get("/get-readings")
async def get_readings(sensor=None, metrics=None, stat=None, time_range=None, request: Request = None):

    # Check for unexpected input parameters
    valid_params = {'sensor', 'metrics', 'stat', 'time_range'}
    for param in request.query_params:
        if param not in valid_params:
            raise HTTPException(status_code=400, detail=f"Unexpected parameter: {param}")

    # CUSTOM SQL REQUEST BUILT DYNAMICALLY
    conn = sqlite3.connect('readings.db')
    c = conn.cursor()
    # variables for SQL WHERE & AND commands
    where_sql = ""
    and_count = 0


    # TIME RANGE PARAM
    # IF time range NOT specified, default to selecting most recent data
    time_filter = "ORDER BY timestamp DESC LIMIT 1"
    # IF time range specified, request will inlcude SQL BETWEEN filter
    if time_range != None:
        # Split time range param into start and end dates
        dates = time_range.split(",")

        # SQL query now includes filter between timestamps
        time_filter = f"timestamp BETWEEN '{dates[0]}' AND '{dates[1]}'"

        # WHERE & AND info updated, WHERE now needed. Number of search filters = 1 (at 2, AND will be needed)
        where_sql = "WHERE "
        and_count += 1


    # STATISTIC PARAM
    # if only taking latest update, no statistic needed (No AVG/MIN etc)
    # in case with no time filter, string will have first letter "O"
    if time_filter[0] == "O":
        stat = ""
    # else if no statistic specified, default to average
    elif stat == None:
        stat = "AVG"
    else:
        # params taken in lower case for simplicity, cast to upper then for SQL command
        stat = stat.upper()


    # METRICS PARAM
    # if none specified, return all
    if metrics == None:
        metrics = "temperature,humidity,wind_speed"

    # determine which metrics to return
    metrics_list = metrics.split(",")
    metrics_sql = ""
    for i in range(len(metrics_list)):
        # if more than 1 metric, add commas
        if i != 0:
            metrics_sql += ", "

        # each metric in metrics_list will be appended to SELECT query, with selected statistic (AVG)
        metrics_sql += f"{stat}({metrics_list[i]})"

        '''
        How this works:
        SELECT {metrics_sql}
        Will look like:
        SELECT AVG(temperature), AVG(humidity)
        '''


    # SENSOR ID PARAM
    # if no sensor specified, exclude field from SQL request
    sensor_filter = ""

    if sensor != None:
        # if sensor specified, SQL request appended
        sensor_filter = f"sensor_id = {sensor} "

        where_sql = "WHERE "
        and_count += 1


    # if both time range and sensor_id specified, and_count will equal 2, requiring SQL AND condition for two statements
    and_sql = ""
    if and_count == 2:
        and_sql = "AND "


    # SQL REQUEST
    try:
        # execute SQL command to query database
        c.execute(f"SELECT {metrics_sql} FROM readings {where_sql} {sensor_filter} {and_sql} {time_filter}")
        resp = c.fetchone()

        # if no data found
        if resp is None:
            return {"error": "No data found for the given query."}

        # response formatted to include metric value pairs
        result = []
        for i in range(len(metrics_list)):
            result.append(metrics_list[i] + ": " + str(resp[i]))

        return {"Weather Readings": result}

    except sqlite3.OperationalError as e:
        return {"error": f"SQL error occurred: {str(e)}"}

    finally:
        conn.close()
