from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, TextChoices, TextField, ImageField, Model, DateTimeField, \
    ForeignKey, SET_NULL

class User(AbstractUser):
    class TYPE(TextChoices):
        ADMIN='admin','Admin',
        USER='user','User',
    secret_word=CharField(max_length=50,null=True,blank=True)
    secret_number=IntegerField(null=True,blank=True)
    passport_number=IntegerField(null=True,blank=True)
    role=CharField(max_length=50,choices=TYPE.choices,default=TYPE.USER)
    about=TextField(null=True,blank=True)
    image=ImageField(upload_to='avatar/%y/%m/%d',null=True,blank=True)