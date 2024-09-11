from django.contrib import admin

# Register your models here.

from .models import Sites

@admin.register(Sites)
class SitesAdmin(admin.ModelAdmin):
    list_display = ('id','status',)
    list_editable = ('status',)
    list_display_links = ('id',)
    
    def get_queryset(self, request):
        user = request.user
        if Sites.objects.filter(user_id=user.id).exists():
            qs = super().get_queryset(request)
            return qs.filter(user_id=user.id)