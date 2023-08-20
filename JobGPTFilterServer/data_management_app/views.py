from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import JobPostModel
from .gpt_qa import gpt_extract_info
import re


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
                             no_sponsorship="blank", require_citizen="blank").save()
        
        return JsonResponse({"message": "Data received and processed!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)

def show_jobs(request):
    # job_list = JobPostModel.objects.exclude(need_clearance="blank").order_by('company_name')
    # filtered_out_list = JobPostModel.objects.filter(need_clearance="blank")
    job_list = JobPostModel.objects.all().order_by('company_name')
    return render(request, 'job_showing_template.html', {'job_list': job_list})


def update_base_on_gpt_answer(jobID, answer):
    if answer.count("@") != 2:
        raise ValueError("answer from GPT is invalid")
    extracted_text = re.search(r'@([^@]+)@', answer).group(1)
    splitted_answers = extracted_text.split(',')
    if len(splitted_answers) != 4:
        raise ValueError("answer from GPT is invalid")
    #yoe
    if splitted_answers[0] != "Unsure":
        JobPostModel.objects.filter(linkedin_job_id=jobID).update(minimum_yoe=float(splitted_answers[0]))
    # clearance
    JobPostModel.objects.filter(linkedin_job_id=jobID).update(need_clearance=splitted_answers[1])
    # NO sponsorship
    JobPostModel.objects.filter(linkedin_job_id=jobID).update(no_sponsorship=splitted_answers[2])
    # citizenship
    JobPostModel.objects.filter(linkedin_job_id=jobID).update(require_citizen=splitted_answers[3])


def start_gpt_filtering(request):
    if request.method == "POST":
        #only deal with unhandled data
        # job_list = JobPostModel.objects.filter(need_clearance="blank")
        job_list = JobPostModel.objects.all()
        for jobObject in job_list:
            jobID = jobObject.linkedin_job_id
            jobDescription = jobObject.job_description
            print("!!!JobDescription: ", jobDescription)
            try:
                answer = gpt_extract_info(jobDescription)
                update_base_on_gpt_answer(jobID, answer)
            except Exception as e:
                print(f"An error occurred while processing job with id '{jobID}': {e}")
                continue

        return JsonResponse({"message": "Button was clicked on the server side!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)