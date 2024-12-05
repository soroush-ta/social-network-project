from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	body = models.TextField()
	slug = models.SlugField()
	title = models.CharField(max_length=100, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created']

	def get_absolute_url(self):
		return reverse('home:post_detail', args=(self.id, self.slug))
	
	
	def total_likes(self):
		return self.like_set.count()
	
	def user_has_liked(self, user):
		return self.like_set.filter(user=user).exists()

	def __str__(self):
		return f'{self.slug} - {self.updated}'
	
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_images/")
	

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField(max_length=400)
	reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rcomments')
	is_reply = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} - {self.body[:30]}'
	
	
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} likes {self.post}'