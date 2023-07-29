from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager

# Create your models here.

class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 값입니다.') # 유효성 검사
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # 해싱 처리 암호화. 복호화 불가
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

# User 모델 커스텀: AbstractUser 상속 (무조건 들어가는 데이터)
class User(AbstractUser):
    phone = models.CharField(verbose_name='전화번호', max_length=11)
    
    objects = UserManager()

# # FK로 User 모델 확장 (자주 사용하지 않는 데이터)
# class UserInfo(models.Model):
#     phone_sub = models.CharField(verbose_name='보조 전화번호', max_length=11)
#     user = models.ForeignKey(to='User', on_delete=models.CASCADE)