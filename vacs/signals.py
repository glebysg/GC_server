from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from vacs.models import Experiment

@receiver(post_save, sender=Experiment)
def model_post_save(sender, instance, created,**kwargs):
    if created:
        # Create students and experts
        # Assign the gestures to the experts
        # Send email to the creator with all the data
        # Write everything in a file too
        pass
