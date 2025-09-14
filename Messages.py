import threading
from queue import Queue
from twilio.rest import Client
import time
import os

# --- Twilio WhatsApp Setup ---
whatsapp_queue = Queue()

SID = ''
TOKEN = ''
FROM_NUMBER = 'whatsapp:+'
TO_NUMBER = 'whatsapp:+'

def queue_whatsapp_message(body: str):
    whatsapp_queue.put(body)

def process_whatsapp_queue():
    client = Client(SID, TOKEN)
    while True:
        try:
            message = whatsapp_queue.get()
            if message is None:
                break  # Graceful shutdown
            client.messages.create(
                body=message,
                from_=FROM_NUMBER,
                to=TO_NUMBER
            )
            whatsapp_queue.task_done()
            time.sleep(1)  # Avoid Twilio rate limits
        except Exception:
            whatsapp_queue.task_done()
            time.sleep(5)  # Backoff on error

# --- Start background message sender thread ---
worker_thread = threading.Thread(target=process_whatsapp_queue, daemon=True)
worker_thread.start()
#queue_whatsapp_message("🚀 WhatsApp message sender started...")
