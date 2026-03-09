from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    def __str__(self):
        return self.comment
