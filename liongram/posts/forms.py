from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from .models import Post

# class PostBaseForm(forms.Form):
#     image = forms.ImageField(label='이미지')
#     content = forms.CharField(label='내용', widget=forms.Textarea, required=True)
#     category = forms.ChoiceField(label='카테고리', choices=(('1', '일반'), ('2', '계정'),))

class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

from django.core.exceptions import ValidationError
class PostCreateForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['image', 'content']
    
    # 유효성 필터링
    def clean_content(self):
        data = self.cleaned_data["content"]
        if "비속어" == data:
            raise ValidationError("비속어는 사용할 수 없습니다.")
        return data

class PostUpdateForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['image', 'content']

class PostDetailForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super(PostDetailForm).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['disabled'] = True