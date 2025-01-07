from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Admin(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])

    def __str__(self):
        return self.name


class Staff(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        default='Other'
    )
    address = models.TextField()

    def __str__(self):
        return self.name


class Course(BaseModel):
    course_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.course_name


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        default='Other'
    )
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='students')

    def __str__(self):
        return self.name


class Subject(BaseModel):
    subject_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='subjects')

    def __str__(self):
        return self.subject_name


class Attendance(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='attendances')
    attendance_date = models.DateField()

    def __str__(self):
        return f"Attendance for {self.subject.subject_name} on {self.attendance_date}"


class AttendanceReport(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='attendance_reports')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='reports')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {'Present' if self.status else 'Absent'}"


class LeaveReport(BaseModel):
    LEAVE_STATUS_CHOICES = [(True, 'Approved'), (False, 'Pending')]
    leave_date = models.DateField()
    leave_message = models.TextField()
    leave_status = models.BooleanField(choices=LEAVE_STATUS_CHOICES, default=False)

    class Meta:
        abstract = True


class LeaveReportStudent(LeaveReport):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='leave_reports')

    def __str__(self):
        return f"Leave by {self.student.name} on {self.leave_date}"


class LeaveReportStaff(LeaveReport):
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='leave_reports')

    def __str__(self):
        return f"Leave by {self.staff.name} on {self.leave_date}"


class Feedback(BaseModel):
    feedback = models.TextField()
    feedback_reply = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class FeedbackStudent(Feedback):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='feedbacks')

    def __str__(self):
        return f"Feedback by {self.student.name}"


class FeedbackStaff(Feedback):
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='feedbacks')

    def __str__(self):
        return f"Feedback by {self.staff.name}"


class Notification(BaseModel):
    message = models.TextField()

    class Meta:
        abstract = True


class NotificationStudent(Notification):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='notifications')

    def __str__(self):
        return f"Notification for {self.student.name}"


class NotificationStaff(Notification):
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='notifications')

    def __str__(self):
        return f"Notification for {self.staff.name}"
