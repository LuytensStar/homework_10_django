from django.forms import ModelForm,TextInput,CharField, ModelChoiceField,ChoiceField
from .models import Quote,Author

class QuoteForm(ModelForm):
    # authors = Author.objects.values_list('fullname', 'fullname')
    author = ModelChoiceField(queryset=Author.objects.all(), label='Author')
    # author = CharField(min_length=3, max_length=200,required=True,widget=TextInput())
    quote = CharField(min_length=3, max_length=1000, required=True, widget=TextInput())
    tags = CharField(min_length=3, max_length=100, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['author', 'quote', 'tags']

class AuthorForm(ModelForm):
    fullname = CharField(max_length=200, required=True, widget=TextInput())
    born_date = CharField(max_length=50, required=False, widget=TextInput())
    born_location = CharField(max_length=50, required=False, widget=TextInput())
    description = CharField(max_length=10000, required=False, widget=TextInput())

    class Meta:
        model=Author
        fields = ['fullname', 'born_date','born_location','description']