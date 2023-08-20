from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import json

def write_to_db(request):
    if request.method == "POST":
        # Load the JSON data from the request body
        data_list = json.loads(request.body.decode("utf-8"))
        # Process each object in the list
        for data_obj in data_list:
            jobId = data_obj.get('linkedinJobId')
            print(jobId)

        return JsonResponse({"message": "Data received and processed!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)