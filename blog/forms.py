from django import forms

class EmailPostForm(forms.Form):
    name = forms .CharField(max_length=50, label='نام', error_messages={'request':'این فیلد الزامی است'})
