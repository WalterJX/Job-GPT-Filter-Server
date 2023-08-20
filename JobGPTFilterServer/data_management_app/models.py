from django.db import models


class JobPostModel(models.Model):
    linkedin_job_id = models.CharField(max_length=15)
    link = models.URLField(max_length=100)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=50)
    job_description = models.TextField()
    minimum_yoe = models.FloatField()  # minimum year of experience required
    need_clearance = models.CharField(max_length=10)  # whether the job needs some kind of security clearance
    sponsorship = models.CharField(max_length=10)  # whether this role provides visa sponsorship
    require_citizen = models.CharField(max_length=10)
