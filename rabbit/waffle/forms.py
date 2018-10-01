from django.forms import ModelForm
from .models import Follow

class FollowForm(ModelForm):
    class Meta:
        model = Follow
        fields = ['follower', 'followee']
