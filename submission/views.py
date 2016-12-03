from django.shortcuts import render
from authentication.models import MyUser
from problem.models import Problem
from django.http import Http404
from note.models import ClassicNote
from django.contrib.auth.decorators import login_required
from .forms import SubmissionForm
from .models import Submission
from util.models import OJ
from .tasks import _submit
from django.http import JsonResponse


def _submit_code(code, language, my_user, problem_id):
    problem = Problem.objects.get(id=problem_id, visible=True)
    remote_oj = OJ.objects.get(name=problem.oj)
    remote_oj_problem_id = problem.oj_id
    submission = Submission.objects.create(code=code, language=language,
                                           user_id=my_user.id, local_problem_id=problem_id,
                                           remote_oj=remote_oj, remote_oj_problem_id=remote_oj_problem_id)
    try:
        _submit.delay(submission.id)
        print(str(submission.result))
        print(str(submission.info))
    except Exception as e:
        print(str(e))
        return JsonResponse({"code": 0, "info": u"提交失败"})
    return JsonResponse({"code": 1, "submission_id": submission.id})


@login_required
def submit_page(request, problem_id):
    """
    前台题目提交页
    """
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.get(user=user)
    try:
        problem = Problem.objects.get(id=problem_id, visible=True)
    except Problem.DoesNotExist:
        raise Http404(u"题目不存在")
    # status==0 表示尚未登陆只能查看
    # status==1 表示已经登陆且与该题没有relation，可以添加classic note
    # status==2 表示已经登陆且与该题有relation，可以修改classic note
    status = 0
    try:
        note = ClassicNote.objects.get(author=my_user, problem=problem)
    except ClassicNote.DoesNotExist:
        note = None
    if user:
        status = 2 if note else 1

    if request.method == 'POST':
        if request.is_ajax():
            form = SubmissionForm(request.POST)
            if form.is_valid():
                code = request.POST.get('code')
                language = request.POST.get('language')
                print(code)
                print(language)
                return _submit_code(code, language, my_user, problem_id)
        else:
            form = SubmissionForm(request.POST)
    else:
        form = SubmissionForm()
    data = {
        'problem': problem,
        'status': status,
        'note': note,
        'form': form,
    }
    return render(request, 'submission/submission_page.html', data)

