from threading import Thread
import pika
import json
from helpers.smsc_helper import SMSCHelper
import os
import logging
import time
import settings
import traceback

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


credentials = pika.PlainCredentials(settings.RABBIT_CREDENTIALS_USER, settings.RABBIT_CREDENTIALS_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_CREDENTIALS_HOST, port=settings.RABBIT_CREDENTIALS_PORT, credentials= credentials))
channel = connection.channel()
channel.exchange_declare('send-sms-topic', durable=True, exchange_type='topic')

def send_sms(ch,method,properties,body):
    logging.info('send poll sms')
    data = json.loads(body.decode('utf-8'))
    connection = SMSCHelper(host=settings.SMS_HOST_USER, port=settings.SMS_HOST_PORT,
                               system_id=settings.SMS_HOST_SYSTEM_ID,
                               password=settings.SMS_HOST_PASSWORD, source_number=data['data']['payload']['source'])
    index = 0
    for item in data['data']['payload']['destinations']:
        _ =  connection.send_short_message(message=data['data']['payload']['body'], destination_number=item)
        logging.info(f'{index}. Send message. To: {item} Body: {data["data"]["payload"]["body"]} From: {data["data"]["payload"]["source"]}')
        index = index + 1
    

def startConsumer():
    connection= pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_CREDENTIALS_HOST))
    logging.info('Consumer is connected')
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
            print(traceback.format_exc())
            time.sleep(1)
            continue