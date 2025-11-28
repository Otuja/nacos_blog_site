from django import forms
from .models import Comment

# form for sharing blog post through email
class EmailPostForm(forms.Form):
    """
    Form for sharing a blog post via email.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SubscribeForm(forms.Form):
    """
    Form for newsletter subscription.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'w-full px-4 py-3 rounded-l-xl border-y border-l border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all'
    }))


# form for commenting on blog post
class CommentForm(forms.ModelForm):
    """
    Form for creating a new comment on a blog post.
    """
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# form for login
class LoginForm(forms.Form):
    """
    Form for user authentication (login).
    """
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        """
        Validates that both username and password are provided.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Both fields are required.")
        
        return cleaned_data
    

class SignupForm(forms.Form):
    """
    Form for user registration (signup).
    """
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        """
        Validates that the password and confirm_password fields match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    

