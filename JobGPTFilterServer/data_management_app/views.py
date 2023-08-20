from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import json
from data_management_app.models import JobPostModel


def write_to_db(request):
    if request.method == "POST":
        # Load the JSON data from the request body
        job_list = json.loads(request.body.decode("utf-8"))
        # Process each object in the list
        for jobObject in job_list:
            jobId = jobObject.get('linkedinJobId')
            job_link = jobObject.get('link')
            job_title = jobObject.get('jobTitle')
            companyName = jobObject.get('companyName')
            jobDescription = jobObject.get('jobDescription')

            if not JobPostModel.objects.filter(linkedin_job_id=jobId).exists():
                JobPostModel(linkedin_job_id=jobId, link=job_link, title=job_title,
                             company_name=companyName, job_description=jobDescription,
                             minimum_yoe=-1, need_clearance="blank",
                             sponsorship="blank", require_citizen="blank").save()
        
        return JsonResponse({"message": "Data received and processed!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)

def show_jobs(request):
    job_list = JobPostModel.objects.all().order_by('company_name')

    return render(request, 'job_showing_template.html', {'job_list': job_list})