from django.urls import reverse

from UniversalPressAgency import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("agency:redactor-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topics = models.ManyToManyField(
        Topic,
        related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="newspapers"
    )

    class Meta:
        ordering = ("title", )

    def __str__(self):
        return f"{self.topics}, {self.title}: {self.content} ({self.published_date})"

    def preview_content(self):
        return " ".join(self.content.split()[:5]) + "..."
