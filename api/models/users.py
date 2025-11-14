from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
import random
import uuid

NEW, CODE_WERIFIED, DONE = ('new', 'code_verified', 'done')

class User(AbstractUser):
    status_choices = (
        (NEW, 'New'),
        (CODE_WERIFIED, 'Code Verified'),
        (DONE, 'Done'),
    )
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    status = models.CharField(max_length=20, default=NEW, choices=status_choices)
    image = models.ImageField(upload_to='user_images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', ])], null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.username
    
    # def create_verify_code(self):
    #     code = "".join([str(random.randint(0, 10000)) for _ in range(4)])
    #     UserConfirmationCode.objects.create(
    #         user_id=self.id,
    #         code=code
    #         )
    #     return code
    
    # def check_username(self):
    #     if not self.username:
    #         username = f'cyberinfo-{uuid.uuid4().__str__().split("-")[-1]}'
    #         self.username = username
    #         self.save()

    # def check_pass(self):
    #     if not self.password:
    #         password = f'password-{uuid.uuid4().__str__().split("-")[-1]}'
    #         self.password = password
    #         self.password = self.set_password(password)

    def save(self, *args, **kwargs):
        if not self.username:
            username = f'username-{uuid.uuid4()}'
            self.username = username

        if not self.password:
            password = f'password-{uuid.uuid4()}'
            self.password = password
            self.set_password(password)

        super(User, self).save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UserConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmations')
    code = models.PositiveIntegerField()
    expire_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.expire_time = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        if timezone.now() > self.expire_time:
            return True
        return False
    
    def __str__(self):
        return f'Code for {self.user.username}: {self.code}'