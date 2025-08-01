from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        READER = "READER", "Reader"
        EDITOR = "EDITOR", "Editor"
        JOURNALIST = "JOURNALIST", "Journalist"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    base_role = Role.READER  # Setting the default role to reader
    role = models.CharField(
        max_length=50,
        choices=Role,
        default=base_role
    )
    sub_journalist = models.ManyToManyField(User, null=True, blank=True, default=None , related_name="subscribers")
    sub_publisher = models.ManyToManyField("bronewsapp.Publisher", null=True, blank=True, default=None, related_name="subscribers") 
    publisher = models.ForeignKey("bronewsapp.Publisher", on_delete=models.CASCADE, null=True, blank=True, default=None)
# limit choices
    def __str__(self):
        return f"{self.user.username} ({self.role})"


