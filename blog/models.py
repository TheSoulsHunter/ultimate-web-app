from django.db import models, connection
from django.contrib.auth.models import User


class Post(models.Model):
    class Meta:
        db_table = 'post'

    title = models.CharField(max_length=180)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_user = models.ForeignKey(User, on_delete=models.PROTECT)

    # likes = models.ManyToManyField(settings.AUTH)

    def get_likes(self):
        args = (self.id, 0)
        cursor = connection.cursor()
        cursor.callproc('count_post_likes', args)
        cursor.execute('SELECT @_count_post_likes_1')
        return cursor.fetchone()[0]


class Project(models.Model):
    class Meta:
        db_table = 'project'

    name = models.CharField(max_length=180)
    github_link = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    def get_likes(self):
        args = (self.id, 0)
        cursor = connection.cursor()
        cursor.callproc('count_project_likes', args)
        cursor.execute('SELECT @count_project_likes_1')
        return cursor.fetchone()[0]


class Comment(models.Model):
    description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'
        ordering = ['-id']

    def __str__(self):
        return 'Comment {} by {}'.format(self.description, self.auth_user.username)

    def get_likes(self):
        args = (self.id, 0)
        cursor = connection.cursor()
        cursor.callproc('count_comment_likes', args)
        cursor.execute('SELECT @_count_comment_likes_1')
        # print(f"[LOG] {self.id} {args}");
        return cursor.fetchone()[0]
        # return cursor.fetchall()


class LikeProject(models.Model):
    class Meta:
        db_table = 'like_project'
        unique_together = ('auth_user', 'project')

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class LikePost(models.Model):
    class Meta:
        db_table = 'like_post'
        unique_together = ('auth_user', 'post')

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class LikeComment(models.Model):
    class Meta:
        db_table = 'like_comment'
        unique_together = ('auth_user', 'comment')

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
