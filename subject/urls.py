from django.urls import path
from subject import views


urlpatterns = [
    path('subjects', views.SubjectCreateListAPIView.as_view(), name='create-subject'),
    path('subject_detail/<str:un_id>',
         views.SubjectDetailAPIView.as_view(), name='subject-detail'),

    path('counties', views.CountyCreateListAPIView.as_view(), name='list_counties'),
    path('county/detail/<str:un_id>',
         views.CountyRetrieveUpdateDestroyAPIVIew.as_view(), name='retrieve-county'),

    path('subcounties', views.SubCountyCreateListAPIView.as_view(),
         name='create_list_subcounties'),
    path('subcounty/detail/<str:un_id>',
         views.SubCountyDetailAPIView.as_view(), name='subcounty-detail'),

    path('constituencies', views.ConstituencyCreateListAPIView.as_view(),
         name='create-constituencies'),
    path('constituency/detail/<str:un_id>',
         views.ConstituencyDetailAPIView.as_view(), name='constituency-detail'),

    path('wards', views.WardCreateListAPIView.as_view(),
         name='create-wards'),
    path('ward/detail/<str:un_id>',
         views.WardDetailAPIView.as_view(), name='ward-detail'),

    path('locations', views.LocationCreateListAPIView.as_view(),
         name='create-locations'),
    path('location/detail/<str:un_id>',
         views.LocationDetailAPIView.as_view(), name='location-detail'),

    path('sublocations', views.SubLocationCreateListAPIView.as_view(),
         name='create-sublocations'),
    path('sublocation/detail/<str:un_id>',
         views.SubLocationDetailAPIView.as_view(), name='sublocation-detail'),

    path('polling-stations', views.PollingStationCreateListAPIView.as_view(),
         name='create-polling-stations'),
    path('polling-station/detail/<str:un_id>',
         views.PollingStationDetailAPIView.as_view(), name='polling-station-detail'),

    path('candidates', views.CandidateCreateListAPIView.as_view(),
         name='create-candidates'),
    path('candidate/detail/<str:un_id>', views.CandidateDetailAPIView.as_view(), name='candidate-detail')
]
