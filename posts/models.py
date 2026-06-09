from django.db import models

class Post(models.Model):

    CATEGORY_CHOICES=[

        # stored, displayed
        ('tech', 'Tech'),
        ('lifestyle', 'Lifestyle'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('finance', 'Finance'),
        ('entertainment', 'Entertainment'),
        ('sports', 'Sports'),
        ('fashion', 'Fashion'),
        ('news', 'News')
    ]

    user=models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class Like(models.Model):

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"