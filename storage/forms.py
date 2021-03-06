from django import forms
from django.utils.translation import ugettext_lazy as _
import re


class AddStgPool(forms.Form):
    name = forms.CharField(error_messages={'required': _('No pool name has been entered')},
                           max_length=20)
    stg_type = forms.CharField(max_length=10)
    target = forms.CharField(error_messages={'required': _('No path has been entered')},
                             max_length=100,
                             required=False)
    source = forms.CharField(error_messages={'required': _('No device has been entered')},
                             max_length=100,
                             required=False)

    def clean_name(self):
        name = self.cleaned_data['name']
        have_symbol = re.match('[^a-zA-Z0-9._-]+', name)
        if have_symbol:
            raise forms.ValidationError(_('The pool name must not contain any special characters'))
        elif len(name) > 20:
            raise forms.ValidationError(_('The pool name must not exceed 20 characters'))
        return name

    def clean_target(self):
        storage_type = self.cleaned_data['stg_type']
        target = self.cleaned_data['target']
        have_symbol = re.match('[^a-zA-Z0-9/]+', target)
        if have_symbol:
            raise forms.ValidationError(_('The type must not contain any special characters'))
        if storage_type == 'dir':
            if not target:
                raise forms.ValidationError(_('No path has been entered'))
        return target

    def clean_source(self):
        storage_type = self.cleaned_data['stg_type']
        source = self.cleaned_data['source']
        have_symbol = re.match('[^a-zA-Z0-9/]+', source)
        if have_symbol:
            raise forms.ValidationError(_('The type must not contain any special characters'))
        if storage_type == 'logical':
            if not source:
                raise forms.ValidationError(_('No device has been entered'))
        return source


class AddImage(forms.Form):
    name = forms.CharField(max_length=20)
    format = forms.ChoiceField(required=True, choices=(('raw', 'raw'), ('qcow', 'qcow'), ('qcow2', 'qcow2')))
    size = forms.IntegerField()

    def clean_name(self):
        name = self.cleaned_data['name']
        have_symbol = re.match('[^a-zA-Z0-9._-]+', name)
        if have_symbol:
            raise forms.ValidationError(_('The image name must not contain any special characters'))
        elif len(name) > 20:
            raise forms.ValidationError(_('The image name must not exceed 20 characters'))
        return name


class CloneImage(forms.Form):
    name = forms.CharField(max_length=20)
    image = forms.CharField(max_length=20)
    convert = forms.BooleanField()
    format = forms.ChoiceField(required=False, choices=(('raw', 'raw'), ('qcow', 'qcow'), ('qcow2', 'qcow2')))

    def clean_name(self):
        name = self.cleaned_data['name']
        have_symbol = re.match('[^a-zA-Z0-9._-]+', name)
        if have_symbol:
            raise forms.ValidationError(_('The image name must not contain any special characters'))
        elif len(name) > 20:
            raise forms.ValidationError(_('The image name must not exceed 20 characters'))
        return name
