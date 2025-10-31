from django.db import models



class Organization(models.Model):
    """
    Model to store organization information.
    """
    organization_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)




class Dataset(models.Model):
    """
    Unified dataset model for harvested CKAN metadata.
    """
    source = models.CharField(max_length=100)              
    source_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author_email = models.CharField(max_length=255, blank=True, null=True)  
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True,
        blank=True, related_name='datasets')


    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['source']),
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return f"[{self.source}] {self.title}"


class Ressource(models.Model):
    """
    Model to store resource information.
    """
    ressource_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    format = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255)
    url = models.TextField(blank=True, null=True)
    url_type = models.CharField(max_length=100, blank=True, null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='ressources')

class Tag(models.Model):
    """
    Model to store tag information.
    """
    tag_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='tags')
