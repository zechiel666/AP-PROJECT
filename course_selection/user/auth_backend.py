from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

#class StudentNumberBackend(ModelBackend):
    #def authenticate(self, request, username=None, password=None, **kwargs):
        #try:
          #  user = User.objects.get(student_number=username)  # Authenticate using student_number
          #  if user.check_password(password):
           #     return user
      #  except User.DoesNotExist:
          #  return None
