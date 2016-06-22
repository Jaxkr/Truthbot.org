from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(OrganizationDomain)
admin.site.register(Organization)
admin.site.register(LoggedOrganizationEdit)
admin.site.register(LoggedOrganizationDomainRemoval)
admin.site.register(OrganizationReview)
admin.site.register(LoggedOrganizationReviewEdit)