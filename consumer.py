from threading import Thread
import pika
import json
from helpers.smsc_helper import SMSCHelper
# from dotenv import load_dotenv
import os

# load_dotenv()
SMS_HOST_USER = '10.90.13.170'
SMS_HOST_PORT = '18013'
SMS_HOST_SYSTEM_ID = 'applista'
SMS_HOST_PASSWORD = 'Lista*21'
RABBIT_CREDENTIALS_USER='guest'
RABBIT_CREDENTIALS_PASSWORD='guest'
RABBIT_CREDENTIALS_HOST='rabbitmq'
RABBIT_CREDENTIALS_PORT=5672

# credentials = pika.PlainCredentials(os.getenv("RABBIT_CREDENTIALS_USER"),os.getenv("RABBIT_CREDENTIALS_PASSWORD"))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBIT_CREDENTIALS_HOST"), port=os.getenv("RABBIT_CREDENTIALS_PORT"), credentials= credentials))
credentials = pika.PlainCredentials(RABBIT_CREDENTIALS_USER, RABBIT_CREDENTIALS_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_CREDENTIALS_HOST, port=RABBIT_CREDENTIALS_PORT, credentials= credentials))
channel = connection.channel()
channel.exchange_declare('send-sms-topic', durable=True, exchange_type='topic')

def send_sms(ch,method,properties,body):
    data = json.loads(body.decode('utf-8'))
    # connection = SMSCHelper(host=os.getenv("SMS_HOST_USER"), port=os.getenv("SMS_HOST_PORT"),
    #                            system_id=os.getenv("SMS_HOST_SYSTEM_ID"),
    #                            password=os.getenv("SMS_HOST_PASSWORD"), source_number=data['data']['payload']['source'])
    connection = SMSCHelper(host=SMS_HOST_USER, port=SMS_HOST_PORT,
                               system_id=SMS_HOST_SYSTEM_ID,
                               password= SMS_HOST_PASSWORD, source_number=data['data']['payload']['source'])
    index = 0
    for item in data['data']['payload']['destinations']:
        _ =  connection.send_short_message(message=item['body'], destination_number=item['destination'])
        print(f'{index}. Send message. To: {item} Body: {data["data"]["payload"]["body"]} From: {data["data"]["payload"]["source"]}')
        index = index + 1
    

def startConsumer():
    connection= pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    #creating channels
    channel= connection.channel()
    #connecting queues to channels
    channel.basic_consume(queue='sms-subscribers',  on_message_callback=send_sms, auto_ack=True)
    #Starting Threads for different channels to start consuming enqueued requests
    Thread(target= channel.start_consuming()).start()

while True:
    try:
        startConsumer()
    except Exception:
        if Exception is KeyboardInterrupt:
            break
        else:
            continue