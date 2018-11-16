from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv

@csrf_exempt
def index(request):
    data = {}
    
    if request.method == "POST":
        query_param = request.POST.get('word', '')

        result = []
        count = 0
        if query_param:
            filename = 'E:\\____Rijo_bkp_Aug_2017\\DevelopmentNew\\djangoapps\\fuzzysearchapp\\word_search.tsv'
            with open(filename, "r") as csvfile:
                datareader = csv.reader(csvfile, delimiter='\t')
                for row in datareader:
                    count += 1
                    if query_param in row[0]:
                        result += [row[0] + "  " + row[1]]

                    if len(result) >= 25:
                        break
        else:
            assert(query_param, 'Query param word shoud not empty!')

        if not result:
            result += ['No result!']

        data = {
            "query_param": query_param,
            "search_count": count,
            "result": result ,
        }
        return JsonResponse(data, safe=False)


    return render(request, 'fuzzysearch/templates/index.html', context=data)

