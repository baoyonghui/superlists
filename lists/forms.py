from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = "You can not have an empty list item"

class ItemForm(forms.models.ModelForm):
    #text = forms.CharField(
    #        widget=forms.fields.TextInput(attrs={
    #            'placeholder': 'Enter a to-do item', 
    #            'class': 'form-control input-lg', 
    #        }),
    #)

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
                'text': forms.fields.TextInput(attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg',
                }), 
        }
        error_messages = {
                'text': {'required': EMPTY_LIST_ERROR}
        }
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
        
