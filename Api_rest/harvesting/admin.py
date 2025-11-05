from django.contrib import admin

from .models import Dataset, Organization, Ressource, Tag

from django.core.management import call_command


admin.site.site_header = "Canwin Dataset Administration"
admin.site.site_title = "Canwin Dataset Admin Portal"
admin.site.index_title = "Welcome to the Dataset Admin Area"
#admin.site.register(Dataset)
admin.site.register(Organization)
admin.site.register(Ressource)
admin.site.register(Tag)



@admin.action(description='Fetch data from CanWin source')
def run_custom_command(modeladmin, request, queryset):
    call_command('fetch_data')  # call your management command
    modeladmin.message_user(request, "Data fetched from CanWin source successfully.")

@admin.register(Dataset)
class MyModelAdmin(admin.ModelAdmin):
    actions = [run_custom_command]
