from django.contrib import admin
from query.models import Query
from rangefilter.filter import DateRangeFilter
# Register your models here.


class QueryAdmin(admin.ModelAdmin):
    ordering = ('-date_updated',)
    list_display = ('patient', 'heading', 'date_updated')
    search_fields = ('patient__email', 'heading', 'body')
    readonly_fields = ('date_published',)

    filter_horizontal = ()
    list_filter = (('date_updated', DateRangeFilter),
                   ('date_published', DateRangeFilter),)
    fieldsets = ()


admin.site.register(Query, QueryAdmin)
