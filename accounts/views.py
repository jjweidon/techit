from django.shortcuts import render,  redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import UserCreateForm, SignupForm

# Create your views here.

def signup_view(request):
    # GET 요청 시 HTML 응답
    if request.method == 'GET':
        form = SignupForm
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
    
    # POST 요청 시 데이터 확인 후 회원 생성
    else:
        form = SignupForm(request.POST)

        if form.is_valid(): # 유효성 검사
            # 회원가입 처리
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password2 = form.cleaned_data['password2']
            instance = form.save()
            return redirect('index')

        else:
            # 리다이렉트
            return redirect('accounts:signup')

def login_view(request):
    # GET, POST 분리
    if request.method == 'GET':
        # 로그인 HTML 응답
        return render(request, 'accounts/login.html', {'form':AuthenticationForm()})
    else:
        # 데이터 유효성 검사
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 비즈니스 로직 처리 - 로그인 처리
            login(request, form.user_cache)
            # 응답
            return redirect('index')
        else:
            # 비즈니스 로직 처리 - 로그인 실패
            # 응답
            return render(request, 'accounts/login.html', {'form':form})

def logout_view(request):
    # 유효성 검사
    if request.user.is_authenticated:
        # 비즈니스 로직 처리
        logout(request)
    # 응답
    return redirect('index')