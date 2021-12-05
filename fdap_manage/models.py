from django.db import models


# Create your models here.
class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_subject = models.CharField(max_length=255, null=False)
    post_contents = models.TextField(null=False)
    post_category = models.CharField(max_length=255, null=True)
    post_tags = models.CharField(max_length=255, null=True)
    post_sector = models.CharField(max_length=255, null=False)
    post_year = models.CharField(max_length=255, null=False)
    report_code = models.CharField(max_length=10, null=False)
    is_success = models.BooleanField(default=False, null=False)
    post_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
