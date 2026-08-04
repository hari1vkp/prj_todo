import json
import pika
from pika import connection

def get_rabbit_connection():
    pakacon=pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=pika.PlainCredentials("guest","guest")
    )
    connection =pika.BlockingConnection(pakacon)
    return connection

 