from django.contrib import admin
from userprofile.models import UserProfile
from rangefilter.filter import DateRangeFilter
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class ProfileAdmin(ImportExportModelAdmin):
    ordering = ('-date_published',)
    list_display = ('user', 'phone', 'qualification',
                    'year_of_ex', 'date_published')
    search_fields = ('user__email', 'phone', 'qualification', 'year_of_ex')
    readonly_fields = ('date_published',)

    filter_horizontal = ()
    list_filter = (('date_published', DateRangeFilter),)
    fieldsets = ()


admin.site.register(UserProfile, ProfileAdmin)
