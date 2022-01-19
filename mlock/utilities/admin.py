from django.contrib import admin

# Register your models here.
from .models import Notes
from .models import Project_universe
from .models import Mysites


admin.site.register(Notes)
admin.site.register(Project_universe)
admin.site.register(Mysites)

