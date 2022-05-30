#!/usr/bin/env python3
import time
import psycopg2
from pgcopy import CopyManager

CONNECTION="postgres://xxxxx:xxxxxx@127.0.0.1:5432/sx_tsdb"

def create_table():  
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    # use the cursor to interact with your database

    query_create_sensors_table = "CREATE TABLE sensors (id SERIAL PRIMARY KEY, type VARCHAR(50), location VARCHAR(50));"
    cursor.execute(query_create_sensors_table)
    # create sensor data hypertable
    query_create_sensordata_table = """CREATE TABLE sensor_data (
                                           time TIMESTAMPTZ NOT NULL,
                                           sensor_id INTEGER,
                                           temperature DOUBLE PRECISION,
                                           cpu DOUBLE PRECISION,
                                           FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                           );"""
    query_create_sensordata_hypertable = "SELECT create_hypertable('sensor_data', 'time');"
    cursor.execute(query_create_sensordata_table)
    cursor.execute(query_create_sensordata_hypertable)

    conn.commit()
    cursor.execute("SELECT 'hello world'")
    print(cursor.fetchone())
    cursor.close()

def insert_data():
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    insert_query1 = "insert into sensors(type,location,senno,name) values('remote','xiamen','en002','远传表');"



def fast_insert(conn):
    cursor = conn.cursor()
    for id in range(1, 4, 1):
        data = (id,)
    # create random data
        simulate_query = """SELECT generate_series(now() - interval '24 hour', now(), interval '5 minute') AS time,
                               %s as sensor_id,
                               random()*100 AS temperature,
                               random() AS cpu
                            """
        cursor.execute(simulate_query, data)
        values = cursor.fetchall()
        cols = ['time', 'sensor_id', 'temperature', 'cpu']
        mgr = CopyManager(conn, 'sensor_data', cols)
        mgr.copy(values)
    conn.commit()

def main():
    conn = psycopg2.connect(CONNECTION)
    # create_table()
    for i in range(1,10000):
        print(time.strftime("%Y-%m-%d %X", time.localtime()),":insert 867 rows successfully....")
        fast_insert(conn)
        time.sleep(1)


main()
