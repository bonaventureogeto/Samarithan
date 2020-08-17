from rest_framework import serializers
from Samarithan.models import Voter, County, SubCounty, Constituency, Ward, Location, PollingStation, Candidate
from authentication.models import User
from authentication.serializers import UserSerializer

class VoterSerializer(serializers.ModelSerializer):
    """ serializer class for voter """

    class Meta:
        model = Voter
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    """ serializer class for county """

    class Meta:
        model = County
        fields = '__all__'


class SubCountySerializer(serializers.ModelSerializer):
    """ serializer class for subcounty """

    class Meta:
        model = SubCounty
        fields = '__all__'


class ConstituencySerializer(serializers.ModelSerializer):
    """ serializer class for constituency """

    class Meta:
        model = Constituency
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    """ serializer class for ward """

    class Meta:
        model = Ward
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    """ serializer class for location """

    class Meta:
        model = Location
        fields = '__all__'

class PollingStationSerializer(serializers.ModelSerializer):
    """ serializer class for polling station """

    class Meta:
        model = PollingStation
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    """ serializer class for Candidate """
    user = UserSerializer(many=False)

    class Meta:
        model = Candidate
        fields = '__all__'


class CommonUserSerializer(serializers.ModelSerializer):
    """ serializer for all users """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'un_id']

