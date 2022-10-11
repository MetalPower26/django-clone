from django.contrib import admin

# Admin delete first if want to compile
# Register your models here.

from .models import Participant, FightParticipant, Team, Member, Band, BandMember

class ParticipantAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 					{'fields': ['name', 'field', 'payment']}),
		('School Information', 	{'fields': ['school', 'grade']}),
		('Private Information', {'fields': ['birthday', 'phone']}),
		('Document', 			{'fields': ['docs']}),
	]
	list_display = ('name', 'field', 'school', 'payment')
	list_filter = ('field', 'school', 'payment')

admin.site.register(Participant, ParticipantAdmin)

class FightAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 					{'fields': ['name', 'field', 'payment']}),
		('School Information', 	{'fields': ['school', 'grade']}),
		('Private Information', {'fields': ['birthday', 'phone', 'weight']}),
		('Document', 			{'fields': ['docs']}),
	]
	list_display = ('name', 'field', 'school', 'payment')
	list_filter = ('field', 'school', 'payment')

admin.site.register(FightParticipant, FightAdmin)

class MemberInline(admin.TabularInline):
	model = Member
	extra = 0

class TeamAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 					{'fields': ['teamname', 'field', 'payment']}),
		('School Information',	{'fields': ['school']}),
		('Leader Information', 	{'fields': ['leader', 'phone']}),
		('Document',			{'fields': ['docs']}),
	]
	inlines = [MemberInline]
	list_display = ('teamname', 'field', 'school', 'payment')
	list_filter = ('field', 'school', 'payment')

admin.site.register(Team, TeamAdmin)

class BandInline(admin.TabularInline):
	model = BandMember
	extra = 0

class BandAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 					{'fields': ['teamname', 'field', 'payment']}),
		('School Information', 	{'fields': ['school']}),
		('Leader Information', 	{'fields': ['leader', 'phone']}),
		('Songs Information',	{'fields': ['song1', 'song2']}),
		('Document', 			{'fields': ['docs']}),
	]
	inlines = [BandInline]
	list_display = ('teamname', 'field', 'school', 'payment')
	list_filter = ('field', 'school', 'payment')

admin.site.register(Band, BandAdmin)