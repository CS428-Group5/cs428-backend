from django.shortcuts import render

# Create your views here.
def meeting_link(request):
    session_id = request.GET.get('session_id', '')
    user_id = request.GET.get('user_id', '')
    full_name = request.GET.get('full_name', '')
    context = {
        "session_id": session_id,
        "user_id": user_id,
        "full_name": full_name
    }
    return render(request, 'video_calling.html', context)