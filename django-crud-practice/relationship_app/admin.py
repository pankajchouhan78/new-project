from django.contrib import admin

from .models import AdharCard, Cources, Designation, Person

# Register your models here.

admin.site.register(AdharCard)
admin.site.register(Person)
admin.site.register(Designation)
admin.site.register(Cources)
