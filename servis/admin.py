from django.contrib import admin

# Register your models here.
from .models  import (JopServis, JopServisCard, AboutServis, AboutServisCard, PriceServis,KontaktServis,
                      PriceServisCard, UstanofkaServis, UstanofkaServisCard, KomandaServis, KomandaServisCard, CategoryServis, CategoryServisCard, KontaktServis, LisenceServis, LisenceServisCard, SavolJavobServis, ContactContentServis)


@admin.register(KontaktServis)
class KontaktServisAdmin(admin.ModelAdmin):
    list_display = ('phone_number',)

@admin.register(ContactContentServis)
class ContactContentServisAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address', 'instagram', 'facebook', 'youtube',)

@admin.register(SavolJavobServis)
class JopServisCardAdmin(admin.ModelAdmin):
    list_display = ('question',)

class JopServisCardInline(admin.TabularInline):
    model = JopServisCard
    extra = 4

@admin.register(JopServis)
class JopServisAdmin(admin.ModelAdmin):
    inlines = [JopServisCardInline]
    list_display = ('header_title', 'header_title_text',)



class AboutServisCardInline(admin.TabularInline):
    model = AboutServisCard
    extra = 4


@admin.register(AboutServis)
class AboutServisAdmin(admin.ModelAdmin):
    inlines = [AboutServisCardInline]
    list_display = ('title',)


class PriceServisCardInline(admin.TabularInline):
    model = PriceServisCard
    extra = 4


@admin.register(PriceServis)
class PriceServisAdmin(admin.ModelAdmin):
    inlines = [PriceServisCardInline]
    list_display = ('title',)

class UstanofkaServisCardInline(admin.TabularInline):
    model = UstanofkaServisCard
    extra = 6



@admin.register(UstanofkaServis)
class UstanofkaServisAdmin(admin.ModelAdmin):
    inlines = [UstanofkaServisCardInline]
    list_display = ('title',)


class KomandaServisCardInline(admin.TabularInline):
    model = KomandaServisCard
    extra = 4



@admin.register(KomandaServis)
class KomandaServisAdmin(admin.ModelAdmin):
    inlines = [KomandaServisCardInline]
    list_display = ('title',)



class CategoryServisCardInline(admin.TabularInline):
    model = CategoryServisCard
    extra = 4

@admin.register(CategoryServis)
class CategoryServisAdmin(admin.ModelAdmin):
    inlines = [CategoryServisCardInline]
    list_display = ('title',)


class LisenceServisCardInline(admin.TabularInline):
    model = LisenceServisCard
    extra = 4


@admin.register(LisenceServis)
class LisenceServisAdmin(admin.ModelAdmin):
    inlines = [LisenceServisCardInline]
    list_display = ('title',)



