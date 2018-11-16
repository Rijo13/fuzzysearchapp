from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
from django.conf import settings


def fuzzy_search(query="", starts_with=False, max_result=25):
    result = []
    words_start_with = {}
    words_contain = {}
    with open(settings.TSV_FILE_LOCATION, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if query in row[0]:
                if row[0].startswith(query):
                    words_start_with[row[0]] = int(row[1])
                else:
                    words_contain[row[0]] = int(row[1])

    from collections import OrderedDict
    from operator import itemgetter
    # sort words_start_with with on length of the string - row[0]
    words_start_with = sorted(words_start_with.items(), key=lambda x:len(x[0]), reverse=False)

    i = 0
    for k,v in words_start_with:
        if i >= max_result:
            break
        result.append(k)
        i += 1

    if len(result)<max_result and not starts_with:
        # sort words_contain with on rank - row[1]
        words_contain = sorted(words_contain.items(), key=itemgetter(1), reverse=True)
        for k,v in words_contain:
            if i >= max_result:
                break
            result.append(k)
            i += 1
    
    return result

@csrf_exempt
def index(request):
    data = {}

    if request.method == "POST":
        query_param = request.POST.get('word', '')

        result = []
        count = 0
        if len(query_param)>=3:
            result = fuzzy_search(query=query_param)
        else:
            assert(query_param, 'Query param word shoud not empty!')

        if not result:
            result += ['No result!']

        data = {
            "query_param": query_param,
            "search_count": count,
            "result": result ,
        }
        # return json respone
        return JsonResponse(data, safe=False)

    # return page
    return render(request, 'fuzzysearch/templates/index.html', context=data)

def auto_complete(request):
    data = {}
    result = []
    query_param = request.GET.get('word', '')
    if len(query_param)>=3:
        result = fuzzy_search(query=query_param, starts_with=True, max_result=5)

    data["result"] = result
    return JsonResponse(data, safe=False)