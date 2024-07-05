from django.contrib import admin
from apps.user.models import *

admin.site.register(User)
admin.site.register(Role)

admin.site.register(Module)
admin.site.register(Permission)
