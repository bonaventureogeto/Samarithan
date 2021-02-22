from django.contrib import admin
from .models import Subject, Candidate, PollingStation, SubLocation, Location, Ward, Constituency, SubCounty, County, PoliticalParty

admin.site.register(Subject)
admin.site.register(Candidate)
admin.site.register(PollingStation)
admin.site.register(SubLocation)
admin.site.register(Location)
admin.site.register(Ward)
admin.site.register(Constituency)
admin.site.register(SubCounty)
admin.site.register(County)
admin.site.register(PoliticalParty)
