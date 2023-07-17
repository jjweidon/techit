from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import ListView
from .models import Post
from django.contrib.auth.decorators import login_required

def index(request):
    post_list = Post.objects.all().order_by('-created_at') # Post 전체 데이터 조회
    context = {
        'post_list': post_list,
    }
    return render(request, 'index.html', context)

def post_list_view(request):
    # post_list = Post.objects.all() # Post 전체 데이터 조회
    post_list = Post.objects.filter(writer=request.user) # Post.writer가 현재 로그인한 유저인 것 조회
    context = {
        'post_list': post_list,
    }
    return render(request, 'posts/post_list.html', context)

def post_detail_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return redirect('index')
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/post_form.html')
    else:
        image = request.FILES.get('image')
        content = request.POST.get('content')
        print(image)
        print(content)
        Post.objects.create(
            image=image,
            content=content,
            writer=request.user,
        )
        return redirect('index')

@login_required
def post_update_view(request, id):
    # post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id, writer=request.user)
    
    if request.method == 'GET':
        context = {'post': post}
        return render(request, 'posts/post_form.html', context)
    
    elif request.method == 'POST':
        new_image = request.FILES.get('image')
        content = request.POST.get('content')

        if new_image:
            post.image.delete()
            post.image = new_image
        post.content = content
        post.save()
        return redirect('posts:post-detail', post.id)

@login_required
def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.writer:
        raise Http404('잘못된 접근입니다.')

    if request.method == 'GET':
        context = {'post': post}
        return render(request, 'posts/post_confirm_delete.html', context)
    else:
        post.delete()
        return redirect('index')



### FBV ###

def url_view(request):
    data = {'code': '001', 'msg': 'ok'}
    return HttpResponse('<h1>here is my url')
    # return JsonResponse(data)

def url_parameter_view(request, username):
    print('this is username')
    print(f'username: {username}')
    print(f'request.GET: {request.GET}') # query string
    return HttpResponse(username)

def function_view(request):
    print(f'request.method: {request.method}')
    if request.method == 'GET':
        (f'request.GET: {request.GET}')
    elif request.method == 'POST':
        (f'request.POST: {request.POST}')
    return render(request, 'view.html')

### CBV ###

class class_view(ListView):
    model = Post
    odering = ['id']
    # template_name = 'cbv_view.html'
    # 위의 template 파일을 지정하면 해당 파일로 이동
    # template_name을 지정하지 않으면 default로 /[app_label]/[model_name]_list.html 로 연결

def function_list_view(request):
    object_list = Post.objects.all().order_by('-id')
    return render(request, 'cbv_view.html', {'object_list': object_list})
