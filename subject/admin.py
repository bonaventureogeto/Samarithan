from django.contrib import admin
from .models import Subject, Candidate, PollingStation, SubLocation, Location, Ward, Constituency, SubCounty, County, PoliticalParty


admin.site.register(County)
admin.site.register(SubCounty)
admin.site.register(Constituency)
admin.site.register(Ward)
admin.site.register(Location)
admin.site.register(SubLocation)
admin.site.register(PollingStation)
admin.site.register(Candidate)
admin.site.register(PoliticalParty)
admin.site.register(Subject)
