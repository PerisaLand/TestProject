from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50, label='نام', error_messages={'request': 'این فیلد الزامی است'})
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {'name': 'نام', 'Email': 'ایمیل', 'Body': 'متن'}
        # exclude = ('post', 'created', 'updated', 'active')

