import pika
import json
from datetime import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='user_events', exchange_type='direct')

channel.queue_declare(queue='login_queue')
channel.queue_declare(queue='log_queue')

channel.queue_bind(exchange='user_events', queue='login_queue', routing_key='user.login')
channel.queue_bind(exchange='user_events', queue='log_queue', routing_key='user.login')
channel.queue_bind(exchange='user_events', queue='log_queue', routing_key='user.upload')
channel.queue_bind(exchange='user_events', queue='log_queue', routing_key='user.logout')

def send_event(user, event):
    message = {
        "user": user,
        "event": event,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    channel.basic_publish(
        exchange='user_events',
        routing_key=event,
        body=json.dumps(message)
    )
    print(f" [x] sent {message}")

send_event ("Cleber", "user.login")
send_event ("Cleber", "user.upload")
send_event ("Cleber", "user.logout")

connection.close()