from datetime import timedelta
import fb.views.webhookView as webhookView

from redis import Redis
from rq_scheduler import Scheduler

redis_server = Redis()
scheduler = Scheduler(connection=redis_server)

def schedulePostToWebhook(bodyAsDict): 
    scheduler.enqueue_in(timedelta(seconds=0 ), webhookView.handlePostToWebhook, bodyAsDict)