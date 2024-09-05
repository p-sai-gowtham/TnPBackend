from django.db import models


# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to="documents", blank=True, null=True)
    type = models.CharField(blank=True, null=True, max_length=225)

    def __str__(self):
        return self.document.name if self.document else "No document"


class JobApplication(models.Model):
    company_name = models.CharField(max_length=255)
    job_description = models.TextField()
    application_deadline = models.DateField()
    drive_date = models.DateField()
    job_application_link = models.URLField(max_length=200)

    def __str__(self):
        return self.company_name


class AppliedApplication(models.Model):
    student = models.ForeignKey(
        "user.User",
        related_name="applied_application",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    job = models.ForeignKey(
        JobApplication,
        related_name="applied_application",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    applied_at = models.DateField()
    has_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} applied for {self.job}"
