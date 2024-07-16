from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # 추가적인 필드를 정의할 수 있습니다.
    pass
