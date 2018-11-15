from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):

	context = {}
	# import pdb; pdb.set_trace()
	import os
	print("current working directory = ", os.getcwd())
	print("is index.html exists in fuzzysearch directory = ", os.path.isfile('fuzzysearch/index.html'))

	return render(request, 'fuzzysearch/templates/index.html', context=context)

def search(request, word):
	query_param = request.GET.get('query', '')
	data = {
		"status": "true",
		"result": [query_param, 1,2,3,4,5] 
	}
	# import json
	# data = json.dumps(data)
	return JsonResponse(data, safe=False)

