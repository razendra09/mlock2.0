from django.contrib import admin

# Register your models here.
from .models import Mlockbot
from .models import Tasks
from .models import Orders
from .models import Outcome


admin.site.register(Mlockbot)
admin.site.register(Tasks)
admin.site.register(Orders)
admin.site.register(Outcome)