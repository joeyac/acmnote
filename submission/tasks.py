from celery import shared_task
from submit_dispatcher.tasks import SubmitDispatcher


@shared_task
def _submit(submission_id):
    SubmitDispatcher(submission_id).submit()
