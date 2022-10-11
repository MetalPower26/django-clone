from django.shortcuts import render

# Create your views here.

def landing(request):
	return render(request, 'index/index.html')

def perlombaan(request):
	return render(request, 'index/perlombaan.html')

def teknis(request, cfield):
	template = 'index/' + cfield + '.html'
	return render(request, template)