from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin

# Register your models here.

@admin.register(OrganizationDomain)
class OrganizationDomainAdmin(VersionAdmin):
    pass

@admin.register(Organization)
class OrganizationAdmin(VersionAdmin):
    pass

@admin.register(OrganizationReview)
class OrganizationReviewAdmin(VersionAdmin):
    pass
