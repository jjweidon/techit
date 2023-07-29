from django.shortcuts import render
import random # lotto
# from django.http import HttpResponse

# Create your views here.
def calculator(request):
    # return HttpResponse('계산기 시작스~~')
    
    # 1. 데이터 확인
    num1 = int(request.GET.get('num1')) 
    num2 = int(request.GET.get('num2'))
    operators = request.GET.get('operators')

    # 2. 연산
    if operators == '+':
        result = num1 + num2
    elif operators == '-':
        result = num1 - num2
    elif operators == '*':
        result = num1 * num2
    elif operators == '/':
        result = num1 / num2
    else:
        result = 0

    # 3. 응답
    return render(request, 'calculator.html', {'result': result})

# 로또 게임 수 (입력)
def lotto_index(request):
    return render(request, 'lotto_index.html')

# 로또 번호 추출 결과 (출력)
def lotto_result(request):
    numbers = [i for i in range(1, 46)]
    game = request.GET.get('game', 1)
    lotto_number = list()
    for _ in range(int(game)):
        lotto_number.append(sorted(random.sample(numbers, 7)))

    return render(request, 'lotto_result.html', {'lotto_number': lotto_number, 'game': game})