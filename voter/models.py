from django.db import models
# from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet
from authentication.models import User




class Voter(models.model):
    """ model for creating voter """
    GENDER_OPTIONS = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    voter_name = models.CharField(max_length=100)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER_OPTIONS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='un_id', db_column='user')
    phone_number = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20, blank=False, unique=True)
    residential_area = models.CharField(max_length=50)

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr of student """
        return self.voter_name



