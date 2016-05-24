from django.db import models


class GithubInformation(models.Model):
    user_email = models.CharField(max_length=200, default="none")
    repository_url = models.CharField(max_length=200)
    repository_owner = models.CharField(max_length=200)
    repository_base = models.CharField(max_length=200)
    repository_head = models.CharField(max_length=200)
    parent_branch_sha = models.CharField(max_length=200, default="none")
    tree_sha = models.CharField(max_length=200, default="none")

    def __str__(self):
        return self.repository_url + "/" + self.repository_head
