from django import forms
from .models import Product, Category, Review


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-0'


class review_form(forms.ModelForm):
    '''
        This class creates instances of a form that will let the user submit
        their review
    '''
    class Meta:
        '''
            Fields
        '''
        model = Review
        fields = ('title', 'body', 'single_rating',)
