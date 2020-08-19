from django.db import models
# from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet
from authentication.models import User


class Subject(models.Model):
    """ model for creating a subject """
    GENDER_OPTIONS = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    subject_name = models.CharField(max_length=100, null=False)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER_OPTIONS)
    phone_number = models.CharField(max_length=20, null=False)
    id_number = models.CharField(max_length=20, blank=False, unique=True)
    residential_area = models.CharField(max_length=50, null=False)

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr of subject """
        return self.subject_name


class County(models.Model):
    """ model for creating a county """
    county_name = models.CharField(max_length=20)

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr for county """
        return self.county_name


class SubCounty(models.Model):
    """ model for creating a sub-county """
    sub_county_name = models.CharField(max_length=20)
    county = models.ForeignKey(County, on_delete=models.CASCADE, to_field='un_id', db_column='county')

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr for sub-county """
        return self.sub_county_name


class Constituency(models.Model):
    """ model for creating a constituency """
    constituency_name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE, to_field='un_id', db_column='county')

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr for constituency """
        return self.constituency_name


class Ward(models.Model):
    """ model for creating a ward """
    ward_name = models.CharField(max_length=20)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, to_field='un_id', db_column='constituency')
    county = models.ForeignKey(County, on_delete=models.CASCADE, to_field='un_id', db_column='user')

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()
    
    def __str__(self):
        """ repr for ward """
        return self.ward_name


class Location(models.Model):
    """ model for creating a Location """
    location_name = models.CharField(max_length=20)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, to_field='un_id', db_column='ward')
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, to_field='un_id', db_column='constituency')
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, to_field='un_id', db_column='sub_county')
    county = models.ForeignKey(County, on_delete=models.CASCADE, to_field='un_id', db_column='county')

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr for location """
        return self.location_name


class PollingStation(models.Model):
    """ model for creating a polling station """
    poll_station_name = models.CharField(max_length=20)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, to_field='un_id', db_column='ward')

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr for polling station """
        return self.poll_station_name



class Candidate(models.Model):
    """ model for creating candidate """
    ELECTIVE_POSITIONS = (
        ('GOV', 'GOVERNER'),
        ('SEN', 'SENATOR'),
        ('WR', 'WOMEN REP'),
        ('MP', 'MEMBER OF PARLIAMENT'),
        ('MCA', 'MEMBER OF COUNTY ASSEMBLY')
    )

    candidate_name = models.CharField(max_length=100)
    vying_position = models.CharField(verbose_name='elective position', max_length=3, choices=ELECTIVE_POSITIONS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='un_id', db_column='user')
    location_name = models.ForeignKey(Location, on_delete=models.CASCADE, to_field='un_id', db_column='location')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, to_field='un_id', db_column='ward')
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, to_field='un_id', db_column='constituency')
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, to_field='un_id', db_column='sub_county')
    county = models.ForeignKey(County, on_delete=models.CASCADE, to_field='un_id', db_column='county')
    polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE, to_field='un_id', db_column='polling_station')

    active_objects = CustomQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self):
        """ repr for candidate """
        return self.candidate_name


