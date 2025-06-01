from django.db.models.signals import post_delete
from django.dispatch import receiver

from leethack.hackathons.models import Hackathon


@receiver(post_delete, sender=Hackathon)
def delete_hackathon_image(sender, instance, **kwargs):
    instance.image.delete(save=False)
