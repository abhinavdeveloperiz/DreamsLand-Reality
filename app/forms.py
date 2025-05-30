from django import forms
from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model=Agent
        fields = ['Profile_picture','username', 'password', 'Phone']
        readonly_fields = ['created_at', 'updated_at','total_sales', 'Total_commission', 'Commission_rate']


class AgentUpdateForm(forms.ModelForm):
    class Meta: 
        model = Agent
        fields = ['Profile_picture','username','Phone']
        widgets = {
            'Profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control'}),
        }