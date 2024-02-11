from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='files/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        super(File, self).save(*args, **kwargs)


class Permission(models.Model):
    VIEW = 'view'
    EDIT = 'edit'
    PERMISSION_CHOICES = [
        (VIEW, 'View'),
        (EDIT, 'Edit'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_permissions')
    permitted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_permissions')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='permissions', null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='permissions', null=True, blank=True)
    permission_type = models.CharField(max_length=4, choices=PERMISSION_CHOICES, default=VIEW)
    
    class Meta:
        unique_together = ('user', 'permitted_user', 'folder', 'file', 'permission_type')
    
    def __str__(self):
        return f"{self.user} -> {self.permitted_user}: {self.permission_type}"
