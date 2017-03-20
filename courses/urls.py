from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from courses.views import CoursesView, AssignmentSubmissionView, TeacherCourseView, AssignmentView, \
    AssignmentSubmissionListView

urlpatterns = [
    url(r'^list/$', login_required(CoursesView.as_view()), name="course-list"),
    url(r'^teach/$', login_required(TeacherCourseView.as_view()), name="teacher-course-list"),

    url(r'^assignment/submission/(?P<assignment_id>\d+)/$', login_required(AssignmentSubmissionView.as_view()),
        name="assignment-submission"),
    url(r'^assignments/list/$', login_required(AssignmentView.as_view()),
        name="assignments-list"),

    url(r'^assignment/submissions/(?P<assignment_id>\d+)$', login_required(AssignmentSubmissionListView.as_view()),
        name="assignments-submissions-list"),
]
