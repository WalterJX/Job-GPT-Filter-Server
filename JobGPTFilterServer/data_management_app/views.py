from collections import defaultdict
from django.db.models import Q
from django.db.models.functions import Length
from django.shortcuts import render
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
    rule = Q(minimum_yoe__gt=-1) & Q(minimum_yoe__lt=4) \
           & ~Q(need_clearance="Yes") & ~Q(no_sponsorship="Yes") & ~Q(require_citizen="Yes")

    job_list = JobPostModel.objects.filter(rule).order_by('company_name')
    remaining_jobs = JobPostModel.objects.exclude(rule).order_by('company_name')
    return render(request, 'job_showing_template.html',
                  {'job_list': job_list, 'filtered_out_job_list': remaining_jobs})


def update_base_on_gpt_answers(jobID, results):
    if len(results) != 4:
        raise ValueError("answer from GPT is invalid")
    #yoe
    if results[0] != "Unsure":
        JobPostModel.objects.filter(linkedin_job_id=jobID).update(minimum_yoe=float(results[0]))
    # clearance
    JobPostModel.objects.filter(linkedin_job_id=jobID).update(need_clearance=results[1])
    # NO sponsorship
    JobPostModel.objects.filter(linkedin_job_id=jobID).update(no_sponsorship=results[2])
    # citizenship
    JobPostModel.objects.filter(linkedin_job_id=jobID).update(require_citizen=results[3])


def gpt_filter_op(jobDescription, jobID):
    # try multiple times as the result may be random, use the result that show up the most times
    attempt_times = 3
    counts = defaultdict(lambda: defaultdict(int))
    for _ in range(attempt_times):
        answer = gpt_extract_info(jobDescription)
        # if answer.count("@") != 2:
        #     raise ValueError("answer from GPT is invalid")
        # splitted_answers = re.search(r'@([^@]+)@', answer).group(1).split(",")
        splitted_answers = answer.split(",")
        if len(splitted_answers) != 4:
            raise ValueError("answer from GPT is invalid")
        for idx, val in enumerate(splitted_answers):
            counts[idx][val] += 1
    # Get the most common answer for each index
    most_common_answers = [max(counts[idx], key=counts[idx].get) for idx in counts]
    update_base_on_gpt_answers(jobID, most_common_answers)

def start_gpt_filtering(request):
    if request.method == "POST":
        #only deal with unhandled data
        job_list = (JobPostModel.objects.filter(need_clearance="blank")
                    .annotate(description_length = Length('job_description'))
                    .order_by('description_length'))
        #sort based on the length in job description


        # job_list = JobPostModel.objects.all()
        for jobObject in job_list:
            jobID = jobObject.linkedin_job_id
            jobDescription = jobObject.job_description
            try:
                print(f"start dealing with job id: {jobID}")
                gpt_filter_op(jobDescription, jobID)
            except Exception as e:
                print(f"An error occurred while processing job with id '{jobID}': {e}")
                continue

        return JsonResponse({"message": "Button was clicked on the server side!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)

def reset_all_status(request):
    if request.method == "POST":
        JobPostModel.objects.update(minimum_yoe=-1)
        JobPostModel.objects.update(need_clearance="blank")
        JobPostModel.objects.update(no_sponsorship="blank")
        JobPostModel.objects.update(require_citizen="blank")
        return JsonResponse({"message": "Reset all job status complete"})
    return JsonResponse({"error": "Invalid request method"}, status=400)
