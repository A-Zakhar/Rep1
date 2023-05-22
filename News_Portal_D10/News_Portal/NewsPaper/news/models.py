from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post = Post.objects.filter(author_id=self.pk, news_or_article=False)
        r1 = 0
        for p in post:
            r1 += p.rating

        comment = Comment.objects.filter(user_id=self.user)
        c1 = 0
        for c in comment:
            c1 += c.rating

        comment = Comment.objects.filter(post__author__user=self.user, post__news_or_article=False)
        c2 = 0
        for c in comment:
            c2 += c.rating

        self.rating = r1 * 3 + c1 + c2
        self.save()

    def __str__(self):
        return f'{self.user.username.title()}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_or_article = models.BooleanField(default=True)  # True - Новость, False - Статья
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        n = 'Новость'
        a = 'Статья'
        return f'{n if self.news_or_article else a} {self.author.user.username} - {self.heading}: {self.text[:20]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()




