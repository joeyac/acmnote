from submission.models import Submission
from .models import JudgeWaitingQueue, JudgeOJ
from django.db import transaction
from django.db.models import F
import time
from submission.result import language_reverse, result
from .oj_submitter.poj import submit_poj
from .tests import solve


class SubmitDispatcher(object):
    def __init__(self, submission_id):
        self.submission = Submission.objects.get(id=submission_id)

    def choose_submit_server(self):
        with transaction.atomic():
            servers = JudgeOJ.objects.select_for_update().filter(
                used_instance_number__lt=F('max_instance_number'), status=True)
            if servers.exists():
                server = servers.first()
                server.used_instance_number = F('used_instance_number') + 1
                server.save()
                return server

    def release_submit_server(self, judge_server_id):
        with transaction.atomic():
            server = JudgeOJ.objects.select_for_update().get(id=judge_server_id)
            server.used_instance_number = F("used_instance_number") - 1
            server.save()

    def submit(self):
        self.submission.judge_start_time = int(time.time() * 1000)
        submit_server = self.choose_submit_server()
        if not submit_server:
            JudgeWaitingQueue.objects.create(submission_id=self.submission.id, )
            return
        try:
            print("start crawler...")
            data = solve(self.submission.remote_oj_submit_id,
                         self.submission.remote_oj_submit_pwd,
                         self.submission.remote_oj_problem_id,
                         language_reverse[self.submission.language],
                         self.submission.code)
            print("end crawler...")
            self.submission.result = data['result']
            if not data:
                self.submission.result = result['remote_error']
            else:
                self.submission.result = result['accepted']
                self.submission.info = data['res']
        except Exception as e:
            self.submission.result = result['system_error']
            self.submission.info = str(e)
        finally:
            self.release_submit_server(submit_server.id)
            self.submission.judge_end_time = int(time.time() * 1000)
            self.submission.save(
                update_fields=["judge_start_time", "result", "info",  "judge_end_time"])

        with transaction.atomic():
            waiting_submissions = JudgeWaitingQueue.objects.select_for_update().all()
            if waiting_submissions.exists():
                # 防止循环依赖
                from submission.tasks import _submit
                waiting_submission = waiting_submissions.first()
                waiting_submission.delete()
                _submit.delay(submission_id=waiting_submission.submission_id)
