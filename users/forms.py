from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.urls import reverse_lazy



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'image']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse_lazy("update_profile", kwargs={'pk': self.instance.pk})
        self.helper.layout = Layout(
            FloatingField("username"),
            FloatingField("email"),
            FloatingField("mobile"),
            Field('image'),
            Div(
                Submit(
                    "submit",
                    "Update",
                    formnovalidate="formnovalidate",
                    css_class="btn btn-outline-success btn-lg",
                ),
                css_class="d-grid gap-2 mb-3",
            ),
        )



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'image', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse_lazy("register")
        self.helper.layout = Layout(
            FloatingField("username"),
            FloatingField("email"),
            FloatingField("mobile"),
            Field("image"),
            FloatingField("password1"),
            FloatingField("password2"),
            Div(
                Submit(
                    "submit",
                    "Register",
                    formnovalidate="formnovalidate",
                    css_class="btn btn-outline-success btn-lg",
                ),
                css_class="d-grid gap-2 mb-3",
            ),
            HTML(
                """
                 <div class="text-center">
                    <p>Already have an account? 
                        <a href="{% url 'login2' %}" 
                            class="link-body-emphasis link-offset-2 link-underline-opacity-25 link-underline-opacity-75-hover">
                                Sign In
                        </a>
                    </p>
                </div>
                 """
            ),
        )


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "login2"
        self.helper.layout = Layout(
            FloatingField("email"),
            FloatingField("password"),
            HTML(
                """
                <div class="mb-3 text-center">
                    <a href="/" 
                        class="link-body-emphasis link-offset-2 link-underline-opacity-25 link-underline-opacity-75-hover">
                        Forgot Password?
                    </a>
                </div>
                 """
            ),
            Div(
                Submit(
                    "submit",
                    "Login",
                    formnovalidate="formnovalidate",
                    css_class="btn btn-outline-success btn-lg",
                ),
                css_class="d-grid gap-2 mb-3",
            ),
            HTML(
                """
                 <div class="text-center">
                    <p>Don't have an account? 
                        <a href="{% url 'register' %}" 
                            class="link-body-emphasis link-offset-2 link-underline-opacity-25 link-underline-opacity-75-hover">
                                Sign Up
                        </a>
                    </p>
                </div>
                 """
            ),
        )

        # TO GET THE layout i needed i changed the original settings of the submit within the function definition to put it
        # field_classes = ""
        """
        self.helper.add_input(
            Div(
                Submit(
                    "submit",
                    "Login",
                    formnovalidate="formnovalidate",
                    css_class="btn btn-lg btn-outline-success",),
                css_class="mt-3"
                )
        )
        """
