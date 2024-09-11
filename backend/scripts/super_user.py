from backend.models import Sites
from account.models import User

for user in User.objects.all():
    if user.is_staff:
        if not(Sites.objects.filter(user_id=user.id).exists()):
            Sites.objects.create(user_id=user.id, status="sts")
            print(f"Created site status for staff user: {user.id}")
