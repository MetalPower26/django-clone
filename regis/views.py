from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Participant, Team, Member, Band, BandMember, FightParticipant
from .fields import SOLO_FIELDS, TEAM_FIELDS, MIN_SIZE, TEAM_SIZE

import base64

# Create your views here.

GRADE_CHOICES = ['10', '11', '12']

label = {'name': 'Nama Peserta', 'school': 'Nama Sekolah', 'grade': 'Kelas', 'phone': 'Nomor Telepon',
		 'birthday': 'Tanggal Lahir', 'docs': 'Dokumen', 'teamname': 'Nama Tim', 'leader': 'Nama Ketua',
		 'song1': 'Lagu Wajib', 'song2': 'Lagu Bebas', 'membername': 'Nama Anggota', 'membergrade': 'Kelas', 
		 'memberbirthday': 'Tanggal Lahir', 'memberrole': 'Peran Anggota',  }

team_dict = {'name':'', 'grade':'', 'birthday':'', 'name_error':'', 'grade_error':'', 'birthday_error':''}
band_dict = {'name':'', 'grade':'', 'birthday':'', 'role':'', 
			 'name_error':'', 'grade_error':'', 'birthday_error':'', 'role_error':''}

def index(request, cfield):

	parameters = {}
	parameters['GRADE_CHOICES'] = GRADE_CHOICES
	parameters['field'] = cfield
	
	if cfield == 'band':

		parameters['TEAM'] = []
		for number in range(1, TEAM_SIZE[cfield]):
			parameters['TEAM'].append(band_dict.copy())

		return render(request, 'regis/band_index.html', parameters)

	elif cfield == 'pencaksilat' or cfield == 'taekwondo':
		return render(request, 'regis/fight_index.html', parameters)
	elif cfield in SOLO_FIELDS:
		return render(request, 'regis/index.html', parameters)
	elif cfield in TEAM_FIELDS:

		parameters['TEAM'] = []
		for number in range(1, TEAM_SIZE[cfield]):
			parameters['TEAM'].append(team_dict.copy())

		return render(request, 'regis/team_index.html', parameters)
	else:
		raise Http404("Page Not Found")

csrftoken = 'csrfmiddlewaretoken'

def notEmpty(member):
	for key in member:
		if key.find('_') == -1 and member[key] == '':
			return False
	return True

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
				phone=data['phone'], docs=request.FILES['docs'], field=cfield, payment=None,
			)

			for member in parameters['TEAM']:
				if notEmpty(member):
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

def BandView(request, cfield):

	parameters = {}
	parameters['GRADE_CHOICES'] = GRADE_CHOICES
	parameters['field'] = cfield

	if request.method == 'POST':

		# create a dictionary of important data from POST
		data = {key:request.POST[key] for key in request.POST if key != csrftoken}

		# construct team
		parameters['TEAM'] = []
		for number in range(1, TEAM_SIZE[cfield]):
			parameters['TEAM'].append(band_dict.copy())

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
				elif datatype == 'memberrole':
					parameters['TEAM'][number - 1]['role'] = data[key]

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
					elif datatype == 'memberrole':
						parameters['TEAM'][number - 1]['error_role'] = label[datatype] + " tidak bisa kosong"
					invalid = True

			elif data[key] == '':

				error = "error_" + key
				parameters[error] = label[key] + " tidak bisa kosong"
				invalid = True

		if invalid:
			return render(request, 'regis/band_index.html', parameters)
		else:

			current_team = Band.objects.create(
				teamname=data['teamname'], school=data['school'], leader=data['leader'],
				phone=data['phone'], docs=request.FILES['docs'], field=cfield, song1=data['song1'],
				song2=data['song2'], payment=None,
			)

			for member in parameters['TEAM']:
				if notEmpty(member):
					Member.objects.create(
						team=current_team, name=member['name'], grade=member['grade'], 
						birthday=member['birthday'], role=member['role']
					)

			# encode decode index

			band_id = current_band.id
			band_id = str(band_id)

			band_id_bytes = band_id.encode("ascii")
			base64_bytes = base64.b64encode(band_id_bytes)
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
				birthday=data['birthday'], docs=request.FILES['docs'], field=cfield, payment=None,
			)

			participant_id = current_participant.id
			participant_id = str(participant_id)

			participant_id_bytes = participant_id.encode("ascii")
			base64_bytes = base64.b64encode(participant_id_bytes)
			base64_string = base64_bytes.decode("ascii")

			return HttpResponseRedirect(reverse('regis:archive', args=(cfield, base64_string)))

def FightView(request, cfield):

	parameters = {}
	parameters['GRADE_CHOICES'] = GRADE_CHOICES
	parameters['field'] = cfield

	if request.method == 'POST':

		# create a dictionary of important data from POST
		data = {key:request.POST[key] for key in request.POST if key != csrftoken}
		print(data)

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
			return render(request, 'regis/fight_index.html', parameters)
		else:

			current_participant = FightParticipant.objects.create(
				name=data['name'], school=data['school'], grade=data['grade'], phone=data['phone'],
				birthday=data['birthday'], docs=request.FILES['docs'], field=cfield, weight=data['weight'],
				payment=None,
			)

			participant_id = current_participant.id
			participant_id = str(participant_id)

			participant_id_bytes = participant_id.encode("ascii")
			base64_bytes = base64.b64encode(participant_id_bytes)
			base64_string = base64_bytes.decode("ascii")

			return HttpResponseRedirect(reverse('regis:archive', args=(cfield, base64_string)))

def data(request, cfield):
	
	if cfield == 'band':
		return BandView(request, cfield)
	elif cfield == 'pencaksilat' or cfield == 'taekwondo':
		return FightView(request, cfield)
	elif cfield in SOLO_FIELDS:
		return ParticipantView(request, cfield)
	elif cfield in TEAM_FIELDS:
		return TeamView(request, cfield)
	else:
		raise Http404("Page Not Found")

def team_archive(request, cfield, objectkey):

	base64_string = objectkey
	base64_bytes = base64_string.encode("ascii")

	team_id_bytes = base64.b64decode(base64_bytes)
	team_id = team_id_bytes.decode("ascii")
	team_id = int(team_id)

	team = Team.objects.get(pk=team_id)

	parameters = {}
	parameters['team'] = team

	return render(request, 'regis/team_archive.html', parameters)

def band_archive(request, cfield, objectkey):

	base64_string = objectkey
	base64_bytes = base64_string.encode("ascii")

	band_id_bytes = base64.b64decode(base64_bytes)
	band_id = band_id_bytes.decode("ascii")
	band_id = int(band_id)

	band = Band.objects.get(pk=band_id)

	parameters = {}
	parameters['band'] = band

	return render(request, 'regis/band_archive.html', parameters)

def participant_archive(request, cfield, objectkey):

	base64_string = objectkey
	base64_bytes = base64_string.encode("ascii")

	participant_id_bytes = base64.b64decode(base64_bytes)
	participant_id = participant_id_bytes.decode("ascii")
	participant_id = int(participant_id)

	participant = Participant.objects.get(pk=participant_id)

	parameters = {}
	parameters['participant'] = participant

	return render(request, 'regis/participant_archive.html', parameters)

def fight_archive(request, cfield, objectkey):

	base64_string = objectkey
	base64_bytes = base64_string.encode("ascii")

	participant_id_bytes = base64.b64decode(base64_bytes)
	participant_id = participant_id_bytes.decode("ascii")
	participant_id = int(participant_id)

	participant = FightParticipant.objects.get(pk=participant_id)

	parameters = {}
	parameters['participant'] = participant

	return render(request, 'regis/fight_archive.html', parameters)

def archive(request, cfield, objectkey):

	if cfield == 'band':
		return band_archive(request, cfield, objectkey)
	elif cfield == 'pencaksilat' or cfield == 'taekwondo':
		return fight_archive(request, cfield, objectkey)
	elif cfield in SOLO_FIELDS:
		return participant_archive(request, cfield, objectkey)
	elif cfield in TEAM_FIELDS:
		return team_archive(request, cfield, objectkey)
	else:
		raise Http404("Page Not Found")