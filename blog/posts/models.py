from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone

from markdown_deux import markdown
from django.utils.safestring import mark_safe

from .utils import get_read_time





class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True,)
    content = models.TextField()
    draft = models.BooleanField(default=True)
    worksheet_file = models.FileField(upload_to = 'worksheets', null = True, blank=True)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(default=0) #assume minute
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    views = models.PositiveIntegerField(default=0) #count views


    objects = PostManager()


    

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["-timestamp", "updated"]

    def get_message_as_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)



def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_message_as_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)

