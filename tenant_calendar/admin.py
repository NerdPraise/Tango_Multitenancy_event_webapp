from django.contrib import admin
from .models import (
    Company, User, ConferenceRoom, Calendar)

# Register your models here.
admin.site.register(Company)
admin.site.register(User)
admin.site.register(ConferenceRoom)
admin.site.register(Calendar)


# Restrict users to respective company except superuser
class CompanyAdminMixin(admin.ModelAdmin):
    '''
    Mixin for objects associated to company
    '''

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs.filter(company_i=request.user.company_i)

    def save_model(self, request, obj, form, change):
        """
        Create objects in the user's company, except for superusers.
        """
        if not change and not request.user.is_superuser:
            assert obj.company_i is None
            obj.company_i = request.user.company_i
        return super().save_model(request, obj, form, change)
