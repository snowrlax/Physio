# Register your models here.

from django.contrib import admin
from physio_app.models import UserProfile, saveEmail, CustomUser, userinfo

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(saveEmail)
admin.site.register(CustomUser)
admin.site.register(userinfo)