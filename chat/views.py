from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render


@login_required
def chat_page(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    return render(
        request,
        "chat.html",
        {
            "other_user": other_user
        }
    )