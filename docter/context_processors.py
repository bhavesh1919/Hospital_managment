from app1.models import Profile, Docter

def doctor_data(request):
    doctor = None

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            doctor = Docter.objects.get(profile=profile)
        except (Profile.DoesNotExist, Docter.DoesNotExist):
            doctor = None

    return {
        "doctor": doctor
    }