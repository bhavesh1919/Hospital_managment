from .models import Patient


def patient_context(request):

    patient = None

    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(profile__user=request.user)
        except Patient.DoesNotExist:
            patient = None

    return {
        "patient": patient
    }