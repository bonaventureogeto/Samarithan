from django.urls import path
from subject import views


urlpatterns = [
    path('subjects', views.SubjectCreateListAPIView.as_view(), name='create-subject'),
    path('subjects/<str:un_id>',
         views.SubjectDetailAPIView.as_view(), name='subject-detail'),

    path('counties', views.CountyCreateListAPIView.as_view(), name='list_counties'),
    path('counties/<str:un_id>',
         views.CountyRetrieveUpdateDestroyAPIVIew.as_view(), name='retrieve-county'),

    path('subcounties', views.SubCountyCreateListAPIView.as_view(),
         name='create_list_subcounties'),
    path('subcounties/<str:un_id>',
         views.SubCountyDetailAPIView.as_view(), name='subcounty-detail'),

    path('constituencies', views.ConstituencyCreateListAPIView.as_view(),
         name='create-constituencies'),
    path('constituencies/<str:un_id>',
         views.ConstituencyDetailAPIView.as_view(), name='constituency-detail'),

    path('wards', views.WardCreateListAPIView.as_view(),
         name='create-wards'),
    path('wards/<str:un_id>',
         views.WardDetailAPIView.as_view(), name='ward-detail'),

    path('locations', views.LocationCreateListAPIView.as_view(),
         name='create-locations'),
    path('locations/<str:un_id>',
         views.LocationDetailAPIView.as_view(), name='location-detail'),

    path('sublocations', views.SubLocationCreateListAPIView.as_view(),
         name='create-sublocations'),
    path('sublocations/<str:un_id>',
         views.SubLocationDetailAPIView.as_view(), name='sublocation-detail'),

    path('polling-stations', views.PollingStationCreateListAPIView.as_view(),
         name='create-polling-stations'),
    path('polling-stations/<str:un_id>',
         views.PollingStationDetailAPIView.as_view(), name='polling-station-detail'),

    path('candidates', views.CandidateCreateListAPIView.as_view(),
         name='create-candidates'),
    path('candidates/<str:un_id>', views.CandidateDetailAPIView.as_view(), name='candidate-detail')
]
