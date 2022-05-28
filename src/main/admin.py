from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from main.models import Meeting, Partner, Topic

# データベースにモデルを明示？
admin.site.register(Meeting)
admin.site.register(Partner)
admin.site.register(Topic)
# admin.site.register(User)
