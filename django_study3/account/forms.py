from django import forms
from django.contrib.auth import password_validation

from account.models import MyUser


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        label="ID",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'help_text': ''
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label="이메일",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일 주소를 입력해주세요'
            }
        ),
    )
    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '숫자와 문자를 포함해 8자리 이상을 입력해주세요'
            }
        ),
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '숫자와 문자를 포함해 8자리 이상을 입력해주세요'
            }
        ),
    )

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                '비밀번호 확인이 일치하지 않습니다.',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

