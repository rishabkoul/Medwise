from django.contrib import admin
from comments.models import Comment
from rangefilter.filter import DateRangeFilter
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    ordering = ('-date_published',)
    list_display = ('written_by', 'commented_on', 'pk', 'date_published')
    search_fields = ('written_by__email', 'commented_on__heading', 'pk')
    readonly_fields = ('date_published',)

    filter_horizontal = ()
    list_filter = (('date_published', DateRangeFilter),)
    fieldsets = ()


admin.site.register(Comment, CommentAdmin)
