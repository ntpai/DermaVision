from django.contrib import admin
from user.models import HospitalProfile

@admin.action(description="Approve Hospital(s)")
def approve_hospital(modeladmin, request, queryset):
    queryset.update(is_approved=True)


class HospitalProfileAdmin(admin.ModelAdmin):
    list_display = ["hospital_name", "license", "is_approved"]
    ordering = ["date_of_registration"]
    actions = [approve_hospital]

admin.site.register(HospitalProfile, HospitalProfileAdmin)