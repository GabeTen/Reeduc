from django.shortcuts import render, get_object_or_404
from .models import Course, Activity, UserActivity
from django.contrib.auth.decorators import login_required

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'cursos/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    activities = course.activities.all()

    for activity in activities:
        UserActivity.objects.get_or_create(user=request.user, activity=activity)

    return render(request, 'cursos/course_detail.html', {
        'course': course,
        'activities': activities,
    })

@login_required
def pending_activities(request):
    pendentes = UserActivity.objects.filter(user=request.user, completed=False)
    return render(request, 'cursos/pending_activities.html', {'pendentes': pendentes})

