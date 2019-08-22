from tom_observations.facilities.lco import LCOBaseObservationForm
from tom_observations.facilities.lco import LCOImagingObservationForm
from tom_observations.facilities.lco import LCOFacility


class LCOCustomObservationForm(LCOBaseObservationForm):
    pass


class LCOCustomFacility(LCOFacility):
    observation_types = [('IMAGING', 'Imaging')]
