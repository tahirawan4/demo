from datetime import datetime
from django.shortcuts import render
from django.views.generic import View

from courses.forms import AssignmentSubmissionForm
from courses.models import Course, Attendance, Assignment, AssignmentSubmission


class CoursesView(View):
    template_name = 'courses.html'

    # noinspection PyMethodMayBeStatic
    def get_course_assignment(self, course):
        assignments = Assignment.objects.filter(course=course)
        assignments_data = []
        for assignment in assignments:
            assignment_submission = AssignmentSubmission.objects.filter(users=self.user, assignment=assignment)
            assignments_data.append({"id": assignment.id,
                                     "title": assignment.title,
                                     "due_date": assignment.due_date,
                                     "expired": False if datetime.now().date() < assignment.due_date else True,
                                     "submitted": True if assignment_submission else False
                                     })
        return assignments_data

    # noinspection PyMethodMayBeStatic
    def create_course_json(self, course, total_attendance, present, absent):
        return {'id': course.id, 'title': course.title, 'total': total_attendance, 'present': present, 'absent': absent,
                "assignments": self.get_course_assignment(course)
                }

    def get(self, request):
        self.user = request.user
        group_name = self.user.groups.all()[0].name
        courses = []
        if group_name == 'Students':
            courses_data = Course.objects.filter(members__id=self.user.id)
            for course in courses_data:
                attendance = Attendance.objects.filter(course=course, student=self.user)
                total_attendance = attendance.count()
                present = attendance.filter(present=True).count()
                absent = total_attendance - present
                courses.append(self.create_course_json(course, total_attendance, present, absent))

        return render(request, self.template_name, {'page': 'courses', 'courses': courses, 'user': 'student'})


class AssignmentSubmissionView(View):
    template_name = 'assignment_submission.html'

    # noinspection PyMethodMayBeStatic
    def get_course_assignment(self, course):
        assignments = Assignment.objects.filter(course=course)
        assignments_data = []
        for assignment in assignments:
            assignment_submission = AssignmentSubmission.objects.filter(users=self.user, assignment=assignment)
            assignments_data.append({"id": assignment.id,
                                     "title": assignment.title,
                                     "due_date": assignment.due_date,
                                     "expired": False if datetime.now().date() < assignment.due_date else True,
                                     "submitted": True if assignment_submission else False
                                     })
        return assignments_data

    # noinspection PyMethodMayBeStatic
    def create_course_json(self, course, total_attendance, present, absent):
        return {'id': course.id, 'title': course.title, 'total': total_attendance, 'present': present, 'absent': absent,
                "assignments": self.get_course_assignment(course)
                }

    def post(self, request, assignment_id):
        form = AssignmentSubmissionForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url', '')
            notes = form.cleaned_data.get('notes', '')
            AssignmentSubmission.objects.create(users=request.user, assignment_id=assignment_id, notes=notes, link=url)

        return render(request, self.template_name, {'page': 'courses', 'form': form})

    def get(self, request, assignment_id):
        form = AssignmentSubmissionForm()
        return render(request, self.template_name, {'page': 'courses', 'form': form})


class TeacherCourseView(View):
    template_name = 'teacher_courses.html'

    # noinspection PyMethodMayBeStatic
    def get_course_assignment(self, course):
        assignments = Assignment.objects.filter(course=course)
        assignments_data = []
        for assignment in assignments:
            assignment_submission = AssignmentSubmission.objects.filter(users=self.user, assignment=assignment)
            assignments_data.append({"id": assignment.id,
                                     "title": assignment.title,
                                     "due_date": assignment.due_date,
                                     "expired": False if datetime.now().date() < assignment.due_date else True,
                                     "submitted": True if assignment_submission else False
                                     })
        return assignments_data

    # noinspection PyMethodMayBeStatic
    def create_course_json(self, course, total_attendance, present, absent):
        return {'id': course.id, 'title': course.title, 'total': total_attendance, 'present': present, 'absent': absent,
                "assignments": self.get_course_assignment(course)
                }

    def get(self, request):
        self.user = request.user
        group_name = self.user.groups.all()[0].name
        courses = []
        if group_name == 'Faculty':
            courses_data = Course.objects.filter(faculty__id=self.user.id)
            for course in courses_data:
                attendance = Attendance.objects.filter(course=course, student=self.user)
                total_attendance = attendance.count()
                present = attendance.filter(present=True).count()
                absent = total_attendance - present
                courses.append(self.create_course_json(course, total_attendance, present, absent))

        return render(request, self.template_name, {'page': 'courses', 'courses': courses, 'user': 'teacher'})


class AssignmentView(View):
    template_name = 'assignments.html'

    # noinspection PyMethodMayBeStatic
    def get_course_assignment(self, course):
        assignments = Assignment.objects.filter(course=course)
        assignments_data = []
        for assignment in assignments:
            assignment_submission = AssignmentSubmission.objects.filter(users=self.user, assignment=assignment)
            assignments_data.append({"id": assignment.id,
                                     "title": assignment.title,
                                     "due_date": assignment.due_date,
                                     "expired": False if datetime.now().date() < assignment.due_date else True,
                                     "submitted": True if assignment_submission else False
                                     })
        return assignments_data

    # noinspection PyMethodMayBeStatic
    def get_assignments_submission(self, course):
        return AssignmentSubmission.objects.filter(assignment__course__id=course.id).count()

    # noinspection PyMethodMayBeStatic
    def create_course_json(self, course, total_attendance, present, absent):
        return {'id': course.id, 'title': course.title, 'total': total_attendance, 'present': present, 'absent': absent,
                "assignments": self.get_course_assignment(course),
                "submissions_count": self.get_assignments_submission(course),
                }

    # noinspection PyMethodMayBeStatic
    def remove_assignment_data(self, assignment_id):
        AssignmentSubmission.objects.filter(assignment__id=assignment_id)
        Assignment.objects.filter(id=assignment_id)

    def get(self, request):
        self.user = request.user
        assignment_id = request.GET.get('assignment_id', '0')
        if assignment_id:
            self.remove_assignment_data(assignment_id)

        group_name = self.user.groups.all()[0].name
        courses = []
        if group_name == 'Faculty':
            courses_data = Course.objects.filter(faculty__id=self.user.id)
            for course in courses_data:
                attendance = Attendance.objects.filter(course=course, student=self.user)
                total_attendance = attendance.count()
                present = attendance.filter(present=True).count()
                absent = total_attendance - present
                courses.append(self.create_course_json(course, total_attendance, present, absent))

        return render(request, self.template_name, {'page': 'assignment', 'courses': courses, 'user': 'teacher'})


class AssignmentSubmissionListView(View):
    template_name = 'list_assignments_submissions.html'

    # noinspection PyMethodMayBeStatic
    def get_assignment_submissions(self, assignment_id):
        assignment_submissions = AssignmentSubmission.objects.filter(assignment__id=assignment_id)
        assignment_data = []
        for assignment_submission in assignment_submissions:
            assignment_data.append({
                "user_name": assignment_submission.users.username,
                "submit_time": assignment_submission.submitted,
                "notes": assignment_submission.notes,
                "link": assignment_submission.link,
                "id": assignment_submission.id

            })
        return assignment_submissions[0].assignment.title, assignment_data

    def get(self, request, assignment_id):
        self.user = request.user
        assignment_title, assignment_submissions = self.get_assignment_submissions(assignment_id)

        return render(request, self.template_name,
                      {'page': 'assignment', 'assignment_submissions': assignment_submissions,
                       'title': assignment_title, 'user': 'teacher'})
