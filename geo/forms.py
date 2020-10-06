
from django.forms import ModelForm
from .models import *

from django import forms



# Create the form class.
class TrackerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # SET 'form-control' class on text fields to make them bootstrap style
        super(TrackerForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.field.widget.input_type in ['text','email']:
                field.field.widget.attrs['class'] = 'form-control'
        # SET required = False to overwrite the form-control, which sets it to True
    class Meta:
        model = TrackerChip
        exclude = ['client']

    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'client_id'}), required=False)


#Have orig and dest select/create loc
#Have the list of trackers for trip be selectable based on trackers owned by that client

#active is True by default
#checkpoint time, checkpoint are set later in events/ webhook

class TripForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # SET 'form-control' class on text fields to make them bootstrap style
        super(TripForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.field.widget.input_type in ['text','email']:
                field.field.widget.attrs['class'] = 'form-control'
        # SET required = False to overwrite the form-control, which sets it to True
    class Meta:
        model = Trip
        exclude = ['check_point_time', 'check_point', 'load']