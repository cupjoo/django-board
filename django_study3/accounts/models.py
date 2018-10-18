from accounts.validators import MinLengthUsernameValidator, UnicodeUsernameValidator
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'ID',
        max_length=30,
        unique=True,
        validators=[
            MinLengthUsernameValidator(),
            UnicodeUsernameValidator(),
        ],
        error_messages={
            'unique': '이미 가입된 ID입니다.'
        }
    )
    email = models.EmailField(
        '이메일',
        unique=True,
        error_messages={
            'unique': '이미 가입된 이메일입니다.'
        }
    )
    phone_number = models.CharField(
        '핸드폰 번호',
        max_length=11,
        unique=True,
        error_messages={
            'unique': '이미 가입된 휴대폰 번호입니다.'
        }
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    # PASSWORD_QUESTION = (
    #     (0, '나의 출생 장소는?'),
    #     (1, '나의 출신 초등학교는?'),
    #     (2, '나의 보물 1호는?'),
    #     (3, '가장 좋아하는 영화는?'),
    #     (4, '가장 좋아하는 음식은?'),
    #     (5, '가장 좋아하는 색깔은?'),
    # )
    # password_answer = models.CharField(
    #     '비밀번호 찾기 답변',
    #     max_length=11,
    # )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username
