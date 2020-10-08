
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
        user = kwargs.pop('user', None)  #form = TripForm(request.POST, request.FILES, user=request.user)

        super(TripForm, self).__init__(*args, **kwargs)

        client = Client.objects.get(user=user)
        tracker_qs = TrackerChip.objects.filter(client=client)
        self.fields['tracker_select'].queryset = tracker_qs #User.objects.filter(pk=user.id)


        for field in self.visible_fields():
            pass
            # if field.field.widget.input_type in ['text','email']:
            #     field.field.widget.attrs['class'] = 'form-control'
        # SET required = False to overwrite the form-control, which sets it to True


        # if self.request.user:
        #     unit_choices=[]
        #     obj = RecipeItem.objects.get(id=self.instance.pk)
        #     fn = obj.usdafood.foodnutrient_set.all()[0]
        #     servings_queryset=NutrientServing.objects.filter(fn=fn)
        #     for s in servings_queryset:
        #         #print s.id
        #         if s.eqv:
        #             ret_str = "%s %s (%s g)"%(s.qty,s.serving.name,s.eqv)
        #         else:
        #             ret_str = "%s"%s.serving.name
        #         unit_choices.append((s.id,ret_str))
        #     #self.fields['units'].choices=unit_choices
        # else:
        #     unit_choices=[]
        # self.fields['units'] = forms.CharField(widget=forms.Select(choices=unit_choices,attrs={'class':'units'}))
    class Meta:
        model = Trip
        # exclude = ['check_point_time', 'check_point', 'load']
        fields = ['orig_display', 'orig_id', 'dest_display', 'dest_id',
                  'tracker_select', 'active', 'ref']#'client_id', 'ref']

    # client_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'client_id'}), required=False)

    orig_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'orig_input'}), required=False)
    dest_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'dest_input'}), required=False)

    tracker_select = forms.ModelMultipleChoiceField(queryset=TrackerChip.objects.all())

    orig_display = forms.CharField(
                    required=False,
                    #queryset = Food.objects.order_by('name'),
                    #widget=forms.CheckboxSelectMultiple
                    widget=forms.TextInput(attrs={'class':'orig_input_display'})
    )

    dest_display = forms.CharField(
                    required=False,
                    #queryset = Food.objects.order_by('name'),
                    #widget=forms.CheckboxSelectMultiple
                    widget=forms.TextInput(attrs={'class':'dest_input_display'})
    )


    ref = forms.CharField(required=False)