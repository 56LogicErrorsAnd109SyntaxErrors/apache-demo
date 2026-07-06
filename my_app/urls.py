from django.urls import path

from . import views

urlpatterns = [
    path("governance-map/", views.graph_page, name="graph_page"),
    path("api/graph-data/", views.graph_data_api, name="graph_data_api"),
    path("governance-map/producers/<str:entity_id>/", views.entity_detail_page, {"entity_type": "producer"}, name="producer_detail"),
    path("governance-map/consumers/<str:entity_id>/", views.entity_detail_page, {"entity_type": "consumer"}, name="consumer_detail"),
    path("governance-map/endpoints/<str:entity_id>/", views.entity_detail_page, {"entity_type": "endpoint"}, name="endpoint_detail"),
]
