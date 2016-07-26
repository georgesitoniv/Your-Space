from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)
    description = models.TextField(max_length=400, blank=True)
    follow = models.ManyToManyField('self', related_name="followers", symmetrical = False)

    def __str__(self):
        return "Profile for user {}".format(self.user.username)
    
    def is_following(self, user):

        if self.follow.filter(id=user.profile.id).exists():
            follows = True
        else:
            follows = False

        return follows



    def is_using_social_auth(self):
        providers = ["facebook", "google", "twitter"]
        if self.user.social_auth.filter(provider__in=providers):
            return True
        else:
            return False

    def get_timeline_users(self):
        followed_users = self.follow.all()
        users = {self.user,}

        for profile in followed_users:
            users.add(profile.user)

        return users