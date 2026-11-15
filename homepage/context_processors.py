from enrollments.models import Enrollment


def global_stats(request):
    return {
        'total_active_enrollments': Enrollment.objects.active().count()
    }