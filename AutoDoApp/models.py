from django.db import models
from django.utils import timezone


class User(models.Model):  # Refactoring -> Change class name

    email = models.CharField(max_length=200, default="none", primary_key=True)
    account_ID = models.CharField(max_length=200, default="none")

    # user_email = models.CharField(max_length=200, default="none")
    # repository_url = models.CharField(max_length=200)
    # repository_owner = models.CharField(max_length=200)
    # repository_base = models.CharField(max_length=200)
    # repository_head = models.CharField(max_length=200)
    # parent_branch_sha = models.CharField(max_length=200, default="none")
    # tree_sha = models.CharField(max_length=200, default="none")
    #
    # def __str__(self):
    #     return self.repository_url + "/" + self.repository_head


class Project(models.Model):
    repository_url = models.CharField(max_length=200)
    repository_owner = models.CharField(max_length=200)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    branch_count = models.IntegerField(default=0)
    last_updated_date = models.DateTimeField(blank=True, null=True, default=timezone.now())
    is_enrolled = models.BooleanField(default=False)

    def update(self):
        self.last_updated_date = timezone.now()
        self.branch_count = self.branch_count.__add__(1)
        self.save()

    def enroll(self):
        self.is_enrolled = True
        self.save()
