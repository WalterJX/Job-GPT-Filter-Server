from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def print_request_details(request):
    # Printing the request method (e.g., GET, POST, etc.)
    print("Request Method:", request.method)

    # Printing the request headers
    print("Request Headers:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    # If it's a POST request, you can print POST data as well
    if request.method == "POST":
        print("POST Data:")
        for key, value in request.POST.items():
            print(f"{key}: {value}")

    # Responding to the client
    return HttpResponse("Request details printed in the console.")