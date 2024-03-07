from confluent_kafka import Producer, Consumer
import socket
import json
import psycopg2
import configparser

config = configparser.ConfigParser.read('./configs.ini')

conn = psycopg2.connect(host=config['postgres']['host'],
                        port=config['postgres']['port'],
                        user=config['postgres']['user'],
                        password=config['postgres']['password'],
                        database=config['postgres']['database'])
cur = conn.cursor()

conf = {'bootstrap.servers': config['kafka']['bootstrap_servers'],
        'group.id': config['kafka']['group_id'],
        'auto.offset.reset': config['kafka']['earliest'],
        'enable.auto.commit': config['kafka']['enable_auto_commit'],
        'client.id': socket.gethostname()}
consumer = Consumer(conf)
consumer.subscribe(config['kafka']['topic_name'])

print("consumer polling starting....")
while True:
    msg = consumer.poll()
    msg_val = msg.value().decode('utf8')
    json_msg_val = json.loads(msg_val)
    try:
        json_val = json_msg_val[config['kafka']['json_key']]
        print(json_val)
        cur.execute(f"INSERT INTO test_table_1(timestamp, test_val) VALUES(current_timestamp, '{json_val}');")
        conn.commit()
    except:
        continue