from django import forms

from catalog.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                continue
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    restricted_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                        'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        exclude = ('date_modified', 'date_created')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data.lower() in self.restricted_words:
            raise forms.ValidationError('Данное название нельзя использовать')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        data_by_word = cleaned_data.lower().split()
        for word in data_by_word:
            if word in self.restricted_words:
                raise forms.ValidationError(
                    'Данное описание содержит запрещённые слова')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class InlineVersionFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        # counter to store number of active versions
        counter = 0
        # loop to check the number of active versions
        for form in self.forms:
            # check if version is active
            if form.cleaned_data.get('is_active'):
                counter += 1
            # raise error if more than one active version exist
            if counter > 1:
                print('Только одна активная версия продукта может быть. '
                      'Выберите одну версию продукта.')
                raise forms.ValidationError(
                    'Только одна активная версия продукта может быть. '
                    'Выберите одну версию продукта.')