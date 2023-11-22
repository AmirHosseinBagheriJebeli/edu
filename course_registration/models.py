from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.CharField(max_length=10, primary_key=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.national_code} \t {self.first_name} {self.last_name}"


class Student(Person):
    student_number = models.CharField(max_length=10, unique=True)
    enrollment_year = models.CharField(max_length=4)
    major = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.national_code} \t {self.first_name} {self.last_name} \t {self.major}"


class Professor(Person):
    staff_number = models.CharField(max_length=10, unique=True)
    hiring_date = models.DateField()
    department = models.ForeignKey("Department", models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.staff_number} \t {self.first_name} {self.last_name} \t {self.department}"


class Department(models.Model):
    name = models.CharField(max_length=255)
    head_of_department = models.ForeignKey(Professor, models.SET_NULL, related_name='head_of_department',
                                           db_column='head', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class ClassRoom(models.Model):
    building = models.CharField(max_length=255)
    floor = models.IntegerField()
    number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    has_video_projector = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.building} \t {self.floor} \t {self.number}"


class Course(models.Model):
    course_code = models.CharField(max_length=4, primary_key=True)
    course_name = models.CharField(max_length=255)
    unit_count = models.IntegerField()

    def __str__(self):
        return f"{self.course_code}\t{self.course_name} \t {self.unit_count}"


class CourseGroup(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='course_code')
    number = models.IntegerField()
    semester = models.CharField(max_length=5)
    offered_by = models.ForeignKey(Professor, models.CASCADE, db_column='offered_by')
    class_room = models.ForeignKey(ClassRoom, models.CASCADE)
    exam_date = models.DateField()
    days = models.BinaryField(max_length=1,
                              db_comment='A 5-bit number, each bit corresponding to a day of the week, '
                                         'and if this bit is 1, the class will be held on that day.')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course}-{self.number}\t{self.semester}\t{self.offered_by}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING)
    course_group = models.ForeignKey(CourseGroup, models.DO_NOTHING)

    def __str__(self):
        return f"{self.student}\t{self.course_group}"


class Assignment(models.Model):
    course_group = models.ForeignKey(CourseGroup, models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.number}\t{self.title}"
