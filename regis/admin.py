from django.contrib import admin

# Register your models here.

from .models import Participant, Member, Team

class ParticipantAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'school']}),
		('Kontak', {'fields': ['grade', 'phone', 'email']}),
		('Dokumen', {'fields':['docs']})
	]

class MemberInline(admin.TabularInline):
	model = Member

class TeamAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['teamname', 'school']}),
		('Informasi Ketua', {'fields': ['leader', 'phone', 'email']}),
		('Dokumen', {'fields':['docs']})
	]
	inlines = [MemberInline]

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Team, TeamAdmin)