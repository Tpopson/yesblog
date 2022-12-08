from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm

from .models import Post, Comment




class SignupForm(UserCreationForm):
    username = forms.CharField(max_length= 50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your prefered Username'}))
    first_name = forms.CharField(max_length= 100)
    last_name = forms.CharField(max_length= 100)
    email = forms.EmailField(max_length= 150)

    
    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'status')
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'cols':10, 'rows':3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}