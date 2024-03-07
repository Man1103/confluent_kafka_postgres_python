from confluent_kafka import Producer, Consumer
import socket
import json
import psycopg2
import configparser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

config = configparser.ConfigParser()
config.read('./configs.ini')

postgres_host=config.get('postgres','host').strip()
postgres_port=config.getint('postgres','port')
postgres_user=config.get('postgres','user').strip()
postgres_password=config.get('postgres','password').strip()
postgres_database=config.get('postgres','database').strip()
print(postgres_host,postgres_port,postgres_user,postgres_password,postgres_database)

kafka_bootstrap_server= config.get('kafka','bootstrap_servers').strip()
kafka_group_id= config.get('kafka','group_id').strip()
kafka_auto_offset_commit= config.get('kafka','auto_offset_reset').strip()
kafka_enable_auto_commit= config.getboolean('kafka','enable_auto_commit')
kafka_topic_name = config.get('kafka','topic_name')
kafka_json_key = config.get('kafka','json_key')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(host=postgres_host,
                        port=postgres_port,
                        user=postgres_user,
                        password=postgres_password,
                        database=postgres_database)
cur = conn.cursor()

conf = {'bootstrap.servers': kafka_bootstrap_server,
        'group.id': kafka_group_id,
        'auto.offset.reset': kafka_auto_offset_commit,
        'enable.auto.commit': kafka_enable_auto_commit,
        'client.id': socket.gethostname()}
consumer = Consumer(conf)
consumer.subscribe(kafka_topic_name)



def run_consumer_polling():
    print("consumer polling starting....")
    while True:
        msg = consumer.poll()
        msg_val = msg.value().decode('utf8')
        json_msg_val = json.loads(msg_val)
        try:
            json_val = json_msg_val[kafka_json_key]
            print(json_val)
            cur.execute(f"INSERT INTO test_table_1(timestamp, test_val) VALUES(current_timestamp, '{json_val}');")
            conn.commit()
        except:
            continue
        
app.post("/run_consumer_polling")
def api_run_consumer_polling():
    run_consumer_polling()
