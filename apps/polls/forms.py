from django import forms

from . import models


class PollCreateForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        fields = ("title", "description")


class PollEditForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        fields = ("title", "description")


class PollDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        fields = tuple()


class PollItemCreateForm(forms.ModelForm):
    class Meta:
        model = models.PollItem
        fields = ("question",)


class PollItemEditForm(forms.ModelForm):
    class Meta:
        model = models.PollItem
        fields = ("question",)
