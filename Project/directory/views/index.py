from django.shortcuts import render


def index(request):
	
	template_name = "directory/index.html"
	context = {
		
	}
	
	return render(request, template_name, context)
	
#def index