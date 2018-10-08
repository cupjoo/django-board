from django.core import validators


class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[a-z0-9]+$'
    message = (
        '알파벳 소문자와 숫자만 허용됩니다.'
    )


class MinLengthUsernameValidator(validators.MinLengthValidator):
    limit_value = 4
    message = (
        '4자 이상 32자 이하로 입력해주세요.'
    )

    def __init__(self):
        super().__init__(self.limit_value)
