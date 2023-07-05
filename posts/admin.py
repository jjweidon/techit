from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class CommnetInline(admin.TabularInline): # StackedInline은 세로 정렬
    model = Comment
    extra = 5
    min_num = 3
    max_num = 5
    verbose_name = '댓글'
    verbose_name_plural = '댓글' # 복수형

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'content', 'created_at', 'view_count', 'writer')
    # list_editable = ('content', )
    list_filter = ('created_at', )
    search_fields = ('id', 'writer__username') # 사용자는 lookup 방식
    search_help_text = '게시판 번호, 사용자 검색이 가능합니다'
    readonly_fields = ('created_at', )
    inlines = (CommnetInline, )

    actions = ('make_published', ) # 관리자 작업 (actions)
    def make_published(modeladmin, request, queryset):
        for item in queryset:
            item.content='운영 규정 위반으로 인한 삭제 처리'
            item.save()

# admin.site.register(Comment)