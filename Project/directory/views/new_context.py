from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from directory.models import Context
from directory.forms import ContextForm


@login_required
def new_context(request):
	
	user = request.user
	
	existing_context = Context.objects.filter(
		uploader=user
	).order_by('-id')
	
	
	if request.method == 'POST':
		
		new_context_form = ContextForm(request.POST)
		
		if 'create_new' in request.POST:
			if new_context_form.is_valid():
				
				# If the user creates a new context
				new_context_instance = new_context_form.save(commit=False)
				new_context_instance.uploader = request.user
				new_context_instance.save()
				
				messages.success(request, "The new context has been created!", extra_tags="success")
				return redirect('new_question', context_id=new_context_instance.id)
			#if
			
			else:
				messages.error(request, new_context_form.errors, extra_tags="danger")
				return redirect('new_context')
			#else
		#if
		
		
		# If user picked an existing context
		elif 'selected' in request.POST:
			selected_django_id = request.POST.get('context_selection')
			
			if selected_django_id and selected_django_id.strip() != "": 
				messages.success(request, "The context has been selected.", extra_tags="success")
				return redirect('new_question', context_id=selected_django_id)
			#if 
			else: 
				messages.error(request, "You must choose a valid context.", extra_tags="danger")
				return redirect('new_context')
			#else
		#elif
		
		
		else:
			messages.error(request, new_context_form.errors, extra_tags="danger")
			return redirect('new_context')
		#else
		
	#if
	
	else:
		new_context_form = ContextForm()
	#else
	
	
	
	
	template_name = "directory/new_context.html"
	context = {
		"existing_context": existing_context,
		"new_context_form": new_context_form,
	}
	
	return render(request, template_name, context)
	
#def new_context