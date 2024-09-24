from django.contrib import admin

# Register your models here.
from .models import JopServis, JopServisCard


class JopServisCardInline(admin.StackedInline):
    model = JopServisCard
    extra = 4

@admin.register(JopServis)
class JopServisAdmin(admin.ModelAdmin):
    inlines = [JopServisCardInline]
    list_display = ('header_title', 'header_title_text',)