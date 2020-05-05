from django.contrib import admin
from .models import Profile
#from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
#from django.contrib.auth.models import Group
from .models import TeamCreation

# Register your models here.
admin.site.register(Profile )


admin.site.register(TeamCreation)

#class GroupInline(admin.StackedInline):
#    model= TeamCreation
#    can_delete= False
#    verbose_name_plural='custom groups'
#    
#class GroupAdmin(BaseGroupAdmin):
#    inlines=(GroupInline, )
#    
##re-register group admin
#admin.site.unregister(Group)
#admin.site.register(Group,GroupAdmin)
