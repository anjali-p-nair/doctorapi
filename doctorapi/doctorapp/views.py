from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Doctor, Slot, Appointment
from .serializers import DoctorSerializer, SlotSerializer, AppointmentSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class SlotAvailabilityViewSet(viewsets.GenericViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def list(self, request, *args, **kwargs):
        doctor_id = self.kwargs.get('doctor_id')
        date = self.kwargs.get('date')
        slots = Slot.objects.filter(doctor_id=doctor_id, date=date)
        serializer = self.serializer_class(slots, many=True)
        return Response(serializer.data)

class BookAppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slot_id = serializer.validated_data['slot'].id
        slot = Slot.objects.get(pk=slot_id)
        if slot.appointments.count() >= slot.max_patients:
            return Response({"error": "Slot is fully booked."}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['appointment_date'] != slot.date:
            return Response({"error": "Appointment date does not match slot date."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
