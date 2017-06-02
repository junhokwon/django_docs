from django.contrib import messages
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404

from polls.models import Question, Choice


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # latest_question_list라는 키로 위 쿼리셋을 전달,
    # polls/index.html을 이용해 render한 결과를 리턴

    # get_list_or_404를 사용한 경우
    latest_question_list = get_list_or_404(
        Question.objects.order_by('-pub_date')[:5]
    )

    context = {
        'latest_question_list': latest_question_list,
    }
    # Template Does Not Exist
    # settings.py에서 TEMPLATE_DIR변수 할당 (BASE_DIR와 os.path.join를 사용)
    # TEMPLATE항목의 DIRS 리스트에 위 변수를 추가
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # question_id가 pk인 Question객체를 가져와
    # context라는 이름을 가진 dict에 'question'이라는 키 값으로 위 변수를 할당
    # 이후 'polls/detail.html'과 context를 렌더한 결과를 리턴

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist as e:
    #     raise Http404('Question does not exist')

    # question.choice_set.
    # Choice.objects.filter(question=question).

    # get_object_or_404를 사용한 경우
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }

    # polls/detail에서 해당 question의 question_text를 출력
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    # detail.html파일을 약간 수정해서 results.html을 만들고
    # 질문에 대한 모든 선택사항의 선택수(votes)를 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }
    # detail.html내부
    #   question을 출력
    #   해당 question의 모든 choice들 (question.choice_set.all) 출력
    #   loop돌며 각 choice의 제목과 votes를 출력
    return render(request, 'polls/results.html', context)


def vote(request, question_id):
    # request의 method가 POST방식일 때,
    if request.method == 'POST':
        # 전달받은 데이터중 'choice'키에 해당하는 값을
        # HttpResponse에 적절히 돌려준다
        data = request.POST
        try:
            choice_id = data['choice']
            choice = Choice.objects.get(id=choice_id)
            choice.votes += 1
            choice.save()
            return redirect('polls:results', question_id)
        except (KeyError, Choice.DoesNotExist):
            # message프레임워크를 사용
            # 지금 모르셔도 됩니다
            # request에 메시지를 저장해놓고 해당 request에 대한
            # response를 돌려줄 때 메시지를 담아 보낸다
            messages.add_message(
                request,
                messages.ERROR,
                "You didn't select a choice",
            )
            return redirect('polls:detail', question_id)
    else:
        return HttpResponse("You're voting on question %s." % question_id)


