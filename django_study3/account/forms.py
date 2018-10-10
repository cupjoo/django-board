from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from account.models import MyUser


class InfoChangeForm(forms.ModelForm):
    old_password = forms.CharField(
        label=_('기존 비밀번호'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label=_('새 비밀번호'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '숫자와 문자를 포함해 8자리 이상을 입력해주세요'
        }),
    )
    new_password2 = forms.CharField(
        label=_('새 비밀번호 확인'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '숫자와 문자를 포함해 8자리 이상을 입력해주세요'
        }),
    )

    class Meta:
        model = MyUser
        fields = ('username', 'phone_number', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'ID',
            'phone_number': '전화번호',
            'email': '이메일',
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user

        # set fields' initial values from user
        initial = kwargs.get('initial', {})
        for key in self.Meta.fields:
            if hasattr(self.user, key):
                initial[key] = getattr(self.user, key)
        kwargs['initial'] = initial
        super(InfoChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                '기존 비밀번호가 일치하지 않습니다.',
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    '비밀번호 확인이 일치하지 않습니다.',
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        self.user = super().save(commit=False)
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '숫자와 문자를 포함해 8자리 이상을 입력해주세요'
        }),
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '숫자와 문자를 포함해 8자리 이상을 입력해주세요'
        }),
    )

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'ID',
            'phone_number': '전화번호',
            'email': '이메일',
        }

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

