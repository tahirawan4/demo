from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import NoArgsCommand

from courses.models import Semester, Course, Assignment, AssignmentSubmission
import datetime


class Command(NoArgsCommand):
    help = "Insert Fixture data!"

    def handle_noargs(self, **options):
        import os

        dev_null = open(os.devnull, 'w')
        print ('updating migrations')
        call_command('migrate', interactive=False, stdout=dev_null, verbosity=0)
        print ('destroying the database')
        call_command('flush', interactive=False, stdout=dev_null)
        call_command('migrate', fake=True, stdout=dev_null, verbosity=0)
        dev_null.close()

        # create groups
        new_group_f, created = Group.objects.get_or_create(name='Faculty')
        new_group_s, created = Group.objects.get_or_create(name='Members')
        new_group_student, created = Group.objects.get_or_create(name='Students')

        super_user = User.objects.create_superuser(username='admin', email='admin@mail.com', password='1234567a')
        # create users
        user1 = User.objects.create_user(username='user1',
                                         email='user1@main.com',
                                         password='1234567a', )
        user1.is_staff = True
        user1.save()
        user2 = User.objects.create_user(username='user2',
                                         email='user2@main.com',
                                         password='1234567a', )
        user2.is_staff = True
        user2.save()
        user3 = User.objects.create_user(username='user3',
                                         email='user3@main.com',
                                         password='1234567a', )
        user3.is_staff = True
        user3.save()
        user4 = User.objects.create_user(username='user4',
                                         email='user4@main.com',
                                         password='1234567a', )
        user4.is_staff = True
        user4.save()
        user5 = User.objects.create_user(username='user5',
                                         email='user5@main.com',
                                         password='1234567a', )
        user5.is_staff = True
        user5.save()
        user6 = User.objects.create_user(username='user6',
                                         email='user6@main.com',
                                         password='1234567a', )
        user6.is_staff = True
        user6.save()

        new_group_f.user_set.add(user1)
        new_group_f.user_set.add(user2)
        new_group_f.user_set.add(user3)
        new_group_f.user_set.add(user4)
        new_group_f.user_set.add(user5)
        new_group_f.user_set.add(user6)
        semester = Semester.objects.create(name='Semester1', year=2017, start=datetime.datetime.now(),
                                           end=datetime.datetime.now())
        course = Course.objects.create(semester=semester, title="OS", section="Morning", number=100,
                                       description='hello')
        course.faculty.add(user1)
        # Create_usersc
        for i in range(50):
            user_name = 'BCS' + str(i)
            email = user_name + "@mail.com"
            user = User.objects.create_user(username=user_name,
                                            email=email,
                                            password='1234567a', )
            user.is_staff = True
            user.save()
            new_group_student.user_set.add(user)
            course.members.add(user)

        users = User.objects.all()
        assignment = Assignment.objects.create(course=course,
                                               title='OSAssignemnt1',
                                               description='Desc',
                                               due_date=datetime.datetime.now())
        AssignmentSubmission.objects.create(users=users[10], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[11], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[12], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[13], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[14], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[15], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[16], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[17], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[18], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[19], assignment=assignment, notes='test')
        AssignmentSubmission.objects.create(users=users[20], assignment=assignment, notes='test')
        print users[20].username
