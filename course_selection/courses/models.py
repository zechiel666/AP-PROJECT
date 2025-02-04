from django.db import models
from django_jalali.db import models as jmodels  # Import Jalali date field to convert Gregorian to solar hijri callender

# Weekday Choices
WEEKDAY_CHOICES = [
    ('شنبه/دوشنبه', 'شنبه/دوشنبه'),
    ('یکشنبه/سشنبه', 'یکشنبه/سشنبه')
]
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Ensure unique department names

    def __str__(self):
        return self.name

class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Ensure unique instructor names
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='instructors')

    def __str__(self):
        return f"{self.name} ({self.department.name})"  # Show instructor + department

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(null=True, max_length=100, blank=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    classDays = models.CharField(max_length=20, choices=WEEKDAY_CHOICES, null=True)  # Stores "Sunday/Tuesday", etc.
    startTime = models.TimeField(null=True)  
    endTime = models.TimeField(null=True)    

    #pishniazi va hamniazi
    pishniaz = models.IntegerField(blank=True , null=True)
    hamniaz = models.IntegerField(blank=True, null=True)

    # Separate Jalali Date and Time
    examDate = jmodels.jDateField(null=True, verbose_name="Exam Date (Jalali)")  # Jalali Date ONLY
    examTime = models.TimeField(null=True, verbose_name="Exam Time")  # Time ONLY

    capacity = models.IntegerField()
    remainingCapacity = models.IntegerField()

    # Foreign Keys
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.name} - {self.department.name} ({self.instructor.name})"

    def save(self, *args, **kwargs):
        """ Ensure remaining capacity starts as full capacity if not set """
        if not self.remainingCapacity:
            self.remainingCapacity = self.capacity
        super().save(*args, **kwargs)