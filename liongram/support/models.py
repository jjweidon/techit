from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
CATEGORY_ONE = '1'
CATEGORY_TWO = '2'
CATEGORY_THREE = '3'

class Faq(models.Model):
    CATEGORY_CHOICES = [
        # (데이터에 들어가는 실제 값, 사용자가 볼 수 있는 출력 값), : 문자 대신 십진수를 처리하여 컴퓨터의 성능 향상 + 다국어 대응
        (CATEGORY_ONE, '일반'),
        (CATEGORY_TWO, '계정'),
        (CATEGORY_THREE, '기타'),
    ]

    title = models.CharField(verbose_name='질문 제목', max_length=80)
    content = models.TextField(verbose_name='질문 내용')
    category = models.CharField(verbose_name='카테고리', max_length=2, choices=CATEGORY_CHOICES)

    created_at = models.DateTimeField(verbose_name='생성 일시', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='최종 수정 일시', auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='faq_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='faq_updated_by')
    # on_delete=models.CASCADE: created_by가 삭제될 때 Faq 모델도 삭제됨
    # related_name='fag_created_by': 역방향 참조 네이밍. 동일한 모델에 연결된 두 속성 => related_name을 따로 설정해야됨.(실무에서 필수)

class Inquiry(models.Model):
    CATEGORY_CHOICES = [
        (CATEGORY_ONE, '일반'),
        (CATEGORY_TWO, '계정'),
        (CATEGORY_THREE, '기타'),
    ]

    category = models.CharField(verbose_name='카테고리', max_length=2, choices=CATEGORY_CHOICES)
    title = models.CharField(verbose_name='질문 제목', max_length=80)
    email = models.EmailField(verbose_name='이메일', blank=True)
    phone = models.CharField(verbose_name='문자메시지', max_length=11, blank=True)
    is_email = models.BooleanField(verbose_name='이메일 수신 여부', default=False)
    is_phone = models.BooleanField(verbose_name='문자메시지 수신 여부', default=False)
    content = models.TextField(verbose_name='문의 내용')
    image = models.ImageField(verbose_name='이미지', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='생성 일시', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='최종 수정 일시', auto_now=True)

    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='inquiry_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='inquiry_updated_by')

class Answer(models.Model):
    content = models.TextField(verbose_name='답변 내용')
    created_at = models.DateTimeField(verbose_name='생성 일시', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='최종 수정 일시', auto_now=True)

    inquiry = models.ForeignKey(to='Inquiry', on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='answer_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='answer_updated_by')