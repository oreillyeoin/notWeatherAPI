from fastapi.testclient import TestClient
from main import app  # Replace `app` with your actual app module if named differently
import sqlite3

client = TestClient(app)

# Method to reset database to allow for accurate testing
def reset_db():
    conn = sqlite3.connect('readings.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS readings")
    c.execute("""CREATE TABLE readings (
                  id integer,
                  sensor_id integer,
                  temperature real,
                  humidity real,
                  wind_speed real,
                  timestamp text
                  )""")
    readings = [
        (3435, 1, 22.5, 55.0, 10.2, "2023-12-10 08:00:00"),
        (7823, 1, 23.1, 56.3, 9.8, "2023-12-10 10:00:00"),
        (1298, 1, 24.2, 58.1, 12.0, "2024-12-10 12:00:00"),
        (6754, 1, 25.0, 60.0, 8.5, "2024-12-10 14:00:00"),
        (9184, 2, 19.8, 65.0, 15.0, "2024-12-11 09:00:00")
    ]
    c.executemany("INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?)", readings)
    conn.commit()
    conn.close()

reset_db()

# Integration test for POST request
def test_add_reading_success():
    reset_db()
    new_reading = {
        "id": 9999,
        "sensor_id": 3,
        "temperature": 20.5,
        "humidity": 60.2,
        "wind_speed": 10.5,
        "timestamp": "2024-12-12T15:00:00"
    }
    response = client.post("/add-reading", json=new_reading)
    assert response.status_code == 200
    assert response.json() == {"Reading Stored Successfully": new_reading}

# Integration test for GET request
def test_get_readings():
    reset_db()
    response = client.get("/get-readings?sensor=1&metrics=temperature,humidity&stat=min&time_range=2024-01-01,2025,01-01")
    assert response.status_code == 200
    assert response.json() == {"Weather Readings": ["temperature: 24.2", "humidity: 58.1"]}

    '''
    Query requests data from sensor 1, specifically in 2024
        (1298, 1, 24.2, 58.1, 12.0, "2024-12-10 12:00:00")
        (6754, 1, 25.0, 60.0, 8.5, "2024-12-10 14:00:00")
        
    The MIN readings for temperature and humidity should be;
        Temperature: 24.2
        Humidity: 58.1
    '''
