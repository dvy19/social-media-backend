from django.db import models

# Create your models here.

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

