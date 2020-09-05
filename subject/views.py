from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from password_generator import PasswordGenerator
from authentication.models import User
from utils.permissions import IsPoliticianAdmin, IsCampaignManager, IsAgent
from subject.models import Subject, County, SubCounty, Constituency, Ward, Location, PollingStation, Candidate
from subject.serializers import SubjectSerializer, CountySerializer, CountyCreateSerializer, SubCountySerializer, SubCountyCreateSerializer, ConstituencySerializer, ConstituencyCreateSerializer, WardSerializer, WardCreateSerializer, LocationSerializer, LocationCreateSerializer, SubLocationSerializer, SubLocationCreateSerializer, PollingStationSerializer, PollingStationCreateSerializer, CandidateSerializer, CandidateCreateSerializer, CommonUserSerializer


class SubjectCreateListAPIView(ListCreateAPIView):
    serializer_class = SubjectSerializer
    permission_classes = (IsAuthenticated, IsAgent, IsCampaignManager, IsPoliticianAdmin)

    @swagger_auto_schema(operation_id="list_subjects")
    def get_queryset(self):
        return Subject.active_objects.all_objects()

    @swagger_auto_schema(operation_id="create_subject")
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data
        response = {
            "subject": data,
            "message": "subject created successfully"
        }

        return Response(response, status=status.HTTP_200_OK)


class SubjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer
    lookup_field = 'un_id'
    permission_classes = (IsAuthenticated, IsPoliticianAdmin, IsCampaignManager)

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return Subject.active_objects.all_objects()

    @swagger_auto_schema(operation_id="subject_detail")
    def get(self, request, un_id):
        subject = self.get_object()
        serializer = self.serializer_class(
            subject
        )
        response = {
            "data": {
                "subject": serializer.data
            }
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_subject_detail")
    def update(self, request, un_id):
        subject = self.get_object()
        serializer = self.serializer_class(
            subject, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "data": {
                "subject": dict(serializer.data),
                "message": "subject updated successfully"
            }
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="destory_subject_detail")
    def destroy(self, request, un_id):
        subject = self.get_object()
        subject.soft_delete()
        subject.is_deleted = True
        subject.save()

        response = {
            "data": {
                "message": "subject deleted successfully"
            }
        }
        return Response(response, status=status.HTTP_200_OK)


class CountyCreateListAPIView(ListAPIView):
    """ list counties"""
    serializer_class = CountySerializer

    @swagger_auto_schema(operation_id="list_counties")
    def get_queryset(self):
        """ list counties """
        return County.active_objects.all_objects()


class CountyCreateAPIView(CreateAPIView):
    """ create for counties """
    serializer_class = CountyCreateSerializer

    @swagger_auto_schema(operation_id="create_county")
    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response(data)


class CountyRetrieveUpdateDestroyAPIVIew(RetrieveUpdateDestroyAPIView):
    """ retrieve and act on counties """
    serializer_class = CountySerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ return a specified queryset depending on the user """
        return County.active_objects.all_objects()

    @swagger_auto_schema(operation_id="update_county_details")
    def update(self, request, un_id):
        """ update a county """

        county = self.get_object()
        data = request.data

        serializer = CountyCreateSerializer(
            county, data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "county": serializer.data,
            "message": "county updated successfully"
        }

        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="destory_county_details")
    def destroy(self, request, un_id):
        """ delete a county """
        county = self.get_object()
        county.soft_delete()
        response = {
            "message": "county deleted successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class SubCountyCreateListAPIView(ListCreateAPIView):
    """ create and list a subcounty """
    serializer_class = SubCountySerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ set the queryset for the subcounty """
        return SubCounty.active_objects.all_objects()

    @swagger_auto_schema(operation_id="list_subcounties")
    def get(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="create_subcounty")
    def post(self, request):
        """ create a subcounty """
        data = request.data

        serializer = SubCountyCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubCountyDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubCountyCreateSerializer
    lookup_field = 'un_id'
    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return SubCounty.active_objects.all_objects()

    @swagger_auto_schema(operation_id="subcounty_detail")
    def get(self, request, un_id):
        subcounty = self.get_object()
        serializer = self.serializer_class(
            subcounty
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_subcounty")
    def update(self, request, un_id):
        subcounty = self.get_object()
        serializer = self.serializer_class(
            subcounty, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="delete_subcounty")
    def destroy(self, request, un_id):
        """ delete one subcounty """
        subcounty = self.get_object()
        subcounty.soft_delete()

        response = {
            "message": "subcounty deleted successfully"
        }

        return Response(response, status=status.HTTP_200_OK)


class ConstituencyCreateListAPIView(ListCreateAPIView):
    """ create and list a constituency """
    serializer_class = ConstituencySerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ set the queryset for the constituency """
        return Constituency.active_objects.all_objects()

    @swagger_auto_schema(operation_id="list_constituencies")
    def get(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="create_constituency")
    def post(self, request):
        """ create a constituency """
        data = request.data

        serializer = ConstituencyCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConstituencyDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ConstituencyCreateSerializer
    lookup_field = 'un_id'
    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return Constituency.active_objects.all_objects()

    @swagger_auto_schema(operation_id="constituency_detail")
    def get(self, request, un_id):
        constituency = self.get_object()
        serializer = self.serializer_class(
            constituency
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_constituency")
    def update(self, request, un_id):
        constituency = self.get_object()
        serializer = self.serializer_class(
            constituency, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="delete_constituency")
    def destroy(self, request, un_id):
        """ delete one constituency """
        constituency = self.get_object()
        constituency.soft_delete()

        response = {
            "message": "constituency deleted successfully"
        }

        return Response(response, status=status.HTTP_200_OK)


class WardCreateListAPIView(ListCreateAPIView):
    """ create and list a Ward """
    serializer_class = WardSerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ set the queryset for the ward """
        return Ward.active_objects.all_objects()

    @swagger_auto_schema(operation_id="list_wards")
    def get(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="create_ward")
    def post(self, request):
        """ create a ward """
        data = request.data

        serializer = WardCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WardDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WardCreateSerializer
    lookup_field = 'un_id'
    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return Ward.active_objects.all_objects()

    @swagger_auto_schema(operation_id="ward_detail")
    def get(self, request, un_id):
        ward = self.get_object()
        serializer = self.serializer_class(
            ward
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_ward")
    def update(self, request, un_id):
        ward = self.get_object()
        serializer = self.serializer_class(
            ward, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="delete_ward")
    def destroy(self, request, un_id):
        """ delete one ward """
        ward = self.get_object()
        ward.soft_delete()

        response = {
            "message": "ward deleted successfully"
        }

        return Response(response, status=status.HTTP_200_OK)


class LocationCreateListAPIView(ListCreateAPIView):
    """ create and list a Location """
    serializer_class = LocationSerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ set the queryset for the Location """
        return Location.active_objects.all_objects()

    @swagger_auto_schema(operation_id="list_locations")
    def get(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="create_location")
    def post(self, request):
        """ create a location """
        data = request.data

        serializer = LocationCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LocationDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LocationCreateSerializer
    lookup_field = 'un_id'
    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return Location.active_objects.all_objects()

    @swagger_auto_schema(operation_id="location_detail")
    def get(self, request, un_id):
        location = self.get_object()
        serializer = self.serializer_class(
            location
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_location")
    def update(self, request, un_id):
        location = self.get_object()
        serializer = self.serializer_class(
            location, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="delete_location")
    def destroy(self, request, un_id):
        """ delete one location """
        location = self.get_object()
        location.soft_delete()

        response = {
            "message": "location deleted successfully"
        }

        return Response(response, status=status.HTTP_200_OK)


class SubLocationCreateListAPIView(ListCreateAPIView):
    """ create and list a sublocation """
    serializer_class = SubLocationSerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ set the queryset for the sublocation """
        return SubLocation.active_objects.all_objects()

    @swagger_auto_schema(operation_id="list_sublocations")
    def get(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="create_sublocation")
    def post(self, request):
        """ create a sublocation """
        data = request.data

        serializer = SubLocationCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubLocationDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubLocationCreateSerializer
    lookup_field = 'un_id'
    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return SubLocation.active_objects.all_objects()

    @swagger_auto_schema(operation_id="sublocation_detail")
    def get(self, request, un_id):
        sublocation = self.get_object()
        serializer = self.serializer_class(
            location
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_sublocation")
    def update(self, request, un_id):
        sublocation = self.get_object()
        serializer = self.serializer_class(
            location, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="delete_sublocation")
    def destroy(self, request, un_id):
        """ delete one sublocation """
        sublocation = self.get_object()
        sublocation.soft_delete()

        response = {
            "message": "sublocation deleted successfully"
        }

        return Response(response, status=status.HTTP_200_OK)


class PollingStationCreateListAPIView(ListCreateAPIView):
    """ create and list a polling station """
    serializer_class = PollingStationSerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ set the queryset for the polling station """
        return PollingStation.active_objects.all_objects()

    @swagger_auto_schema(operation_id="list_polling_stations")
    def get(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="create_polling_station")
    def post(self, request):
        """ create a polling station """
        data = request.data

        serializer = PollingStationCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PollingStationDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PollingStationCreateSerializer
    lookup_field = 'un_id'
    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return PollingStation.active_objects.all_objects()

    @swagger_auto_schema(operation_id="polling_station_detail")
    def get(self, request, un_id):
        polling_station = self.get_object()
        serializer = self.serializer_class(
            polling_station
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_polling_station")
    def update(self, request, un_id):
        polling_station = self.get_object()
        serializer = self.serializer_class(
            polling_station, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="delete_polling_station")
    def destroy(self, request, un_id):
        """ delete one polling_station """
        polling_station = self.get_object()
        polling_station.soft_delete()

        response = {
            "message": "polling station deleted successfully"
        }

        return Response(response, status=status.HTTP_200_OK)


class CandidateCreateListAPIView(ListCreateAPIView):
    """ create and list a Candidate """
    serializer_class = CandidateSerializer
    lookup_field = 'un_id'

    def get_queryset(self):
        """ set the queryset for the Candidate """
        return Candidate.active_objects.all_objects()

    @swagger_auto_schema(operation_id="list_candidates")
    def get(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="create_candidate")
    def post(self, request):
        """ create a candidate """
        data = request.data

        serializer = CandidateCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CandidateDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CandidateCreateSerializer
    lookup_field = 'un_id'
    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ 
        return a different queryset depending on who is logged in
        """

        return Candidate.active_objects.all_objects()

    @swagger_auto_schema(operation_id="candidate_detail")
    def get(self, request, un_id):
        candidate = self.get_object()
        serializer = self.serializer_class(
            candidate
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="update_candidate")
    def update(self, request, un_id):
        candidate = self.get_object()
        serializer = self.serializer_class(
            candidate, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="delete_candidate")
    def destroy(self, request, un_id):
        """ delete one candidate """
        candidate = self.get_object()
        candidate.soft_delete()

        response = {
            "message": "candidate deleted successfully"
        }

        return Response(response, status=status.HTTP_200_OK)
