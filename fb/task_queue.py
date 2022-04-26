from datetime import timedelta
import fb.views.webhookView as webhookView

from redis import Redis
from rq_scheduler import Scheduler

redis_server = Redis()
scheduler = Scheduler(connection=redis_server)

# https://stackoverflow.com/questions/56200672

def schedulePostToWebhook(bodyAsDict): 
    print("about to schedule post to webhook")
    scheduler.enqueue_in(timedelta(seconds=0.1), webhookView.handlePostToWebhook, bodyAsDict)