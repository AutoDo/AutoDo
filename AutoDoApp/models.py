from django.db import models
from django.utils import timezone


class User(models.Model):  # Refactoring -> Change class name

    email = models.CharField(max_length=200, default="none", primary_key=True)
    account_ID = models.CharField(max_length=200, default="none")
    access_token = models.CharField(max_length=200, default="none")

    def __init__(self, email, account_ID):
        super(User, self).__init__()
        if "@" not in email:
            raise ValueError("Email should be well-formatted")
        else:
            self.email = email

        if len(email) < 10:
            raise ValueError("Email should have sufficient length")
        else:
            self.email = email

        if len(account_ID) < 5:
            raise ValueError("account ID should have more than 5 length")
        else:
            self.account_ID = account_ID

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
    description = models.TextField(null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    branch_count = models.IntegerField(default=0)
    last_updated_date = models.DateTimeField(blank=True, null=True)
    project_license = models.CharField(max_length=200)
    is_enrolled = models.BooleanField(default=False)

    def update(self):
        self.last_updated_date = timezone.now()
        if type(self.branch_count) is int:
            self.branch_count = self.branch_count.__add__(1)
        else:
            raise TypeError('Type Error')
        self.save()

    def enroll(self):
        if type(self.is_enrolled) is bool:
            self.is_enrolled = True
            self.save()
        else:
            raise TypeError('Type Error')

    def desc_update(self, desc):
        if type(self.description) is str and type(desc) is str:
            self.description = desc
            self.save()
        else:
            raise TypeError('Type Error')
