from rest_framework import routers
from django.urls import path, include
from .views import DoctorViewSet, SlotAvailabilityViewSet, BookAppointmentViewSet

app_name = 'doctorapp'


router = routers.DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'book-appointment', BookAppointmentViewSet, basename='book-appointment')


urlpatterns = [
    path('', include(router.urls)),

]
