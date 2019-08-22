from django import forms
from crispy_forms.layout import Div

from tom_observations.facilities.lco import LCOBaseObservationForm
from tom_observations.facilities.lco import LCOImagingObservationForm
from tom_observations.facilities.lco import LCOFacility


class LCOCustomObservationForm(LCOBaseObservationForm):
    rotator_angle = forms.FloatField(min_value=0.0, initial=0.0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instrument_type'] = forms.ChoiceField(choices=self.instrument_choices(), widget=forms.HiddenInput())

    def layout(self):
        return Div(
            Div(
                'name', 'proposal', 'ipp_value', 'observation_mode', 'start', 'end',
                css_class='col'
            ),
            Div(
                'filter', 'instrument_type', 'exposure_count', 'exposure_time', 'max_airmass', 'rotator_angle',
                css_class='col'
            ),
            css_class='form-row'
        )

    def instrument_choices(self):
        # return [(k, v['name']) for k, v in self._get_instruments().items() if 'SPECTRA' in v['type']]
        return [('2M0-FLOYDS', '2.0 meter FLOYDS')]

    # NRES does not take a slit, and therefore needs an option of None
    def filter_choices(self):
        return set([
            (f['code'], f['name']) for ins in self._get_instruments().values() for f in
            ins['optical_elements'].get('slits', [])
            ] + [('None', 'None')])

    def _build_instrument_config(self):
        instrument_config = super()._build_instrument_config()
        if self.cleaned_data['filter'] != 'None':
            instrument_config['optical_elements'] = {
                'slit': self.cleaned_data['filter']
            }
        else:
            instrument_config.pop('optical_elements')
        instrument_config['rotator_mode'] = 'VFLOAT'
        instrument_config['extra_params'] = {
            'rotator_angle': self.cleaned_data['rotator_angle']
        }

        return instrument_config


class LCOCustomFacility(LCOFacility):
    observation_types = [('IMAGING', 'Imaging'), ('SPECTROSCOPY', 'Spectroscopy')]

    def get_form(self, observation_type):
        if observation_type == 'IMAGING':
            return LCOImagingObservationForm
        elif observation_type == 'SPECTROSCOPY':
            return LCOCustomObservationForm
