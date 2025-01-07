import pika
from fastapi import FastAPI

app = FastAPI()

# Event bus functions
def publish_event(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange="", routing_key=queue_name, body=message)
    connection.close()

def consume_event(queue_name, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    def on_message(channel, method, properties, body):
        callback(body)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    channel.start_consuming()

@app.post("/alert/threshold")
def send_alert(glucose_level: float):
    if glucose_level < 70 or glucose_level > 180:
        publish_event("alerts", "Glucose level critical: {glucose_level}")
        return {"status": "Alert sent"}
    return {"status": "Normal glucose level"}
