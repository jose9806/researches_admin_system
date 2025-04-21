from django import forms
from gruplac.models import DatosBasicos


class BusquedaInvestigadorForm(forms.Form):
    TIPO_CHOICES = [
        ("general", "Búsqueda general"),
        ("nombre", "Nombre"),
        ("id", "ID CvLAC"),
        ("orcid", "ORCID"),
    ]

    termino = forms.CharField(
        label="Término de búsqueda",
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "vTextField", "placeholder": "Ingrese nombre, ID o ORCID"}
        ),
    )

    tipo_busqueda = forms.ChoiceField(
        label="Tipo de búsqueda",
        choices=TIPO_CHOICES,
        initial="general",
        widget=forms.Select(attrs={"class": "vSelectField", "style": "height: auto;"}),
    )


class AsignacionGrupoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We'll populate the choices in the admin view to avoid cross-database issues
        self.fields["grupo_id"].widget.choices = [("", "---------")]

    grupo_id = forms.ChoiceField(
        label="Grupo de investigación",
        required=True,
        widget=forms.Select(attrs={"class": "vSelectField"}),
    )

    observaciones = forms.CharField(
        label="Observaciones",
        required=False,
        widget=forms.Textarea(attrs={"class": "vLargeTextField", "rows": 3}),
    )
