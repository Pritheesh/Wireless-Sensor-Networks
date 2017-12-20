from django import forms

TOPOLOGY_CHOICES = (
    (1, "Square"),
    (2, "Circle")
)


class InputForm(forms.Form):
    nodes = forms.CharField(label="Nodes")
    degree = forms.CharField(label="Degree")
    topology = forms.ChoiceField(choices=TOPOLOGY_CHOICES)
    # with_edges = forms.BooleanField(required=False)
    # min_and_max = forms.BooleanField(required=False)

