from django.contrib import admin
from .models import User, Role, Address, Organization
import datetime

class UserAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return ['email', 'user_type']
    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        return User.objects.filter(user_type='ServiceProvider')


# class UserprofielAdmin(admin.ModelAdmin):

#     def queryset(self, request):
#         # import pdb;pdb.set_trace()
#         qs = super(UserprofielAdmin, self).queryset(request)
#         # import pdb;pdb.set_trace()
#         qs.user.queryset = User.objects.filter(user_type='ServiceProvider')
#         return qs        


#     def get_list_display(self, request):
#         # import pdb;pdb.set_trace()
#         return ['user', 'user_role']

#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#         if db_field.name == "user":
#             kwargs["queryset"] = User.objects.filter(user_type='ServiceProvider')
#         return super(UserprofielAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(User, UserAdmin)
# admin.site.register(UserProfile, UserprofielAdmin)
admin.site.register(Role)
admin.site.register(Address)
admin.site.register(Organization)
