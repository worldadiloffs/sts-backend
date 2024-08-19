from cProfile import Profile
from django.contrib import admin



from .models import User, PhoneOtp , GouseUser , Xodim, UserAddress

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("first_name",  "last_name", "phone",  "author", "is_special_user", 'two_step_password',"password", 'last_login', 'date_joined', 'is_staff', )
    list_display = (
        "phone", "first_name",
        "last_name", "is_staff",
        "author", "is_special_user",
    )
    list_filter = ("is_staff", "is_superuser", "groups", )
    search_fields = ("first_name", "last_name", "phone")
    ordering = ("is_superuser", "is_staff", "pk")


@admin.register(PhoneOtp)
class PhoneOtpAdmin(admin.ModelAdmin):
    list_display = (
        "phone", "otp", "count", "verify",
    )
    search_fields = ("phone", "otp",)

admin.site.register(GouseUser)



@admin.register(Xodim)
class XodimlarAdmin(admin.ModelAdmin):
    list_display =( "name", )

