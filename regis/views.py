from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Participant, Team, Member

import base64

# Create your views here.

GRADE_CHOICES = ['10', '11', '12']
SOLO_FIELDS   = ['catur', 'menyanyi']
TEAM_FIELDS   = ['basket', 'voli']
MIN_SIZE 	  = {'basket':5, 'voli':6}
TEAM_SIZE     = {'basket':8, 'voli':9}

label = {'name': 'Nama Peserta', 'school': 'Nama Sekolah', 'grade': 'Kelas', 'phone': 'Nomor Telepon',
		 'birthday': 'Tanggal Lahir', 'docs': 'Dokumen', 'teamname': 'Nama Tim', 'leader': 'Nama Ketua', 
		 'membername': 'Nama Anggota', 'membergrade': 'Kelas', 'memberbirthday': 'Tanggal Lahir'}

team_dict = {'name':'', 'grade':'', 'birthday':'', 'name_error':'', 'grade_error':'', 'birthday_error':''}

def index(request, cfield):

	parameters = {}
	parameters['GRADE_CHOICES'] = GRADE_CHOICES
	parameters['field'] = cfield
	
	if cfield in SOLO_FIELDS:
		parameters['current_grade'] = ''
		return render(request, 'regis/index.html', parameters)
	else:

		parameters['TEAM'] = []
		for number in range(1, TEAM_SIZE[cfield]):
			parameters['TEAM'].append(team_dict.copy())

		return render(request, 'regis/team_index.html', parameters)

csrftoken = 'csrfmiddlewaretoken'

def TeamView(request, cfield):

	parameters = {}
	parameters['GRADE_CHOICES'] = GRADE_CHOICES
	parameters['field'] = cfield

	if request.method == 'POST':

		# create a dictionary of important data from POST
		data = {key:request.POST[key] for key in request.POST if key != csrftoken}

		# construct team
		parameters['TEAM'] = []
		for number in range(1, TEAM_SIZE[cfield]):
			parameters['TEAM'].append(team_dict.copy())

		for key in data:

			if key[:6] == 'member':
				# number is zero-based
				datatype, number = key.split('_')
				number = int(number)

				if datatype == 'membername':
					parameters['TEAM'][number - 1]['name'] = data[key]
				elif datatype == 'membergrade':
					parameters['TEAM'][number - 1]['grade'] = data[key]
				elif datatype == 'memberbirthday':
					parameters['TEAM'][number - 1]['birthday'] = data[key]

			else:
				curr = "current_" + key
				parameters[curr] = data[key]

		invalid = False

		for key in data:

			if key[:6] == 'member':
				# number is zero-based
				datatype, number = key.split('_')
				number = int(number)

				if data[key] == '' and number <= MIN_SIZE[cfield]:
					if datatype == 'membername':
						parameters['TEAM'][number - 1]['error_name'] = label[datatype] + " tidak bisa kosong"
					elif datatype == 'membergrade':
						parameters['TEAM'][number - 1]['error_grade'] = label[datatype] + " tidak bisa kosong"
					elif datatype == 'memberbirthday':
						parameters['TEAM'][number - 1]['error_birthday'] = label[datatype] + " tidak bisa kosong"
					invalid = True

			elif data[key] == '':

				error = "error_" + key
				parameters[error] = label[key] + " tidak bisa kosong"
				invalid = True

		if invalid:
			return render(request, 'regis/team_index.html', parameters)
		else:

			current_team = Team.objects.create(
				teamname=data['teamname'], school=data['school'], leader=data['leader'],
				phone=data['phone'], docs=request.FILES['docs']
			)

			for member in parameters['TEAM']:
				Member.objects.create(
					team=current_team, name=member['name'], grade=member['grade'], birthday=member['birthday']
				)

			# encode decode index

			team_id = current_team.id
			team_id = str(team_id)

			team_id_bytes = team_id.encode("ascii")
			base64_bytes = base64.b64encode(team_id_bytes)
			base64_string = base64_bytes.decode("ascii")

			return HttpResponseRedirect(reverse('regis:archive', args=(cfield, base64_string)))

def ParticipantView(request, cfield):

	parameters = {}
	parameters['GRADE_CHOICES'] = GRADE_CHOICES
	parameters['field'] = cfield

	if request.method == 'POST':

		# create a dictionary of important data from POST
		data = {key:request.POST[key] for key in request.POST if key != csrftoken}

		# construct team

		for key in data:
			curr = "current_" + key
			parameters[curr] = data[key]

		invalid = False

		for key in data:

			if data[key] == '':

				error = "error_" + key
				parameters[error] = label[key] + " tidak bisa kosong"
				invalid = True

		if invalid:
			return render(request, 'regis/index.html', parameters)
		else:

			current_participant = Participant.objects.create(
				name=data['name'], school=data['school'], grade=data['grade'], phone=data['phone'],
				birthday=data['birthday'], docs=request.FILES['docs']
			)

			participant_id = current_participant.id
			participant_id = str(participant_id)

			participant_id_bytes = participant_id.encode("ascii")
			base64_bytes = base64.b64encode(participant_id_bytes)
			base64_string = base64_bytes.decode("ascii")

			return HttpResponseRedirect(reverse('regis:archive', args=(cfield, base64_string)))

def data(request, cfield):
	
	if cfield in SOLO_FIELDS:
		return ParticipantView(request, cfield)
	elif cfield in TEAM_FIELDS:
		return TeamView(request, cfield)

price_index = {
	'basket': 100, 'catur': 200, 'menyanyi': 300, 'voli': 400
}

def team_archive(request, cfield, objectkey):

	base64_string = objectkey
	base64_bytes = base64_string.encode("ascii")

	team_id_bytes = base64.b64decode(base64_bytes)
	team_id = team_id_bytes.decode("ascii")
	team_id = int(team_id)

	team = Team.objects.get(pk=team_id)

	parameters = {}
	parameters['team'] = team
	parameters['payment'] = 150000 + price_index[cfield] + team.id

	return render(request, 'regis/team_archive.html', parameters)

def participant_archive(request, cfield, objectkey):

	base64_string = objectkey
	base64_bytes = base64_string.encode("ascii")

	participant_id_bytes = base64.b64decode(base64_bytes)
	participant_id = participant_id_bytes.decode("ascii")
	participant_id = int(participant_id)

	participant = Participant.objects.get(pk=participant_id)

	parameters = {}
	parameters['participant'] = participant
	parameters['payment'] = 150000 + price_index[cfield] + participant.id

	return render(request, 'regis/participant_archive.html', parameters)

def archive(request, cfield, objectkey):

	if cfield in SOLO_FIELDS:
		return participant_archive(request, cfield, objectkey)
	else:
		return team_archive(request, cfield, objectkey)
