from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_delete, sender=User)
def delete_user_files(sender, instance, **kwargs):
    if instance.profile_picture.name != settings.DEFAULT_PROFILE_PICTURE:
        instance.profile_picture.delete(save=False)
    if instance.profile_background.name != settings.DEFAULT_PROFILE_BACKGROUND:
        instance.profile_background.delete(save=False)
