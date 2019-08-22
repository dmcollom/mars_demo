

ALERCE_URL = 'http://alerce.online'
ALERCE_SEARCH_URL = 'http://ztf.alerce.online/query'

RF_CLASSIFIERS = [(None, "None")] + [(k, k) for k in ["CEPH", "DSCT", "EB", "LPV", "RRL", "SNe", "Other"]]
STAMP_CLASSIFIERS = [(None, "None")] + [(k, k) for k in ["AGN", "SN", "VS", "asteroid", "bogus"]]


# query_parameters:{
#     filters:{
#         oid: "ZTFXXXXXX",
#         nobs: { 
#             min: int
#             max: int
#         },
#         classrf: ["CEPH","DSCT","EB","LPV","RRL","SNe","Other"] or int,
#         pclassrf: float [0-1],
#         classearly: ["AGN","SN","VS","asteroid","bogus"] or int,
#         pclassearly: float [0-1],
#     },
#     coordinates:{
#         ra: float degrees,
#         dec: float degrees,
#         sr: float degrees
#     },
#     dates:{
#         firstmjd: {
#          min: float mjd,
#          max: float mjd
#         }
#     }
# }


class AlerceQueryForm(GenericQueryForm):
    pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            self.common_layout,
            Fieldset(
                'Non-Detections',
                Div(
                    Div(
                        'nobs__gt',
                        css_class='col',
                    ),
                    Div(
                        'nobs__lt',
                        css_class='col',
                    ),
                    css_class="form-row",
                )
            ),
            Fieldset(
                'Classification Filters',
                Div(
                    Div(
                        'classrf',
                        'classearly',
                        css_class='col'
                    ),
                    Div(
                        'pclassrf',
                        'pclassearly',
                        css_class='col',
                    ),
                    css_class="form-row",
                )
            ),
            Fieldset(
                'Location Filters',
                'ra',
                'dec',
                'sr'
            ),
            Fieldset(
                'Time Filters',
            ),
            Div(
                    Div(
                        'mjd__gt',
                        css_class='col',
                    ),
                    Div(
                        'mjd__lt',
                        css_class='col',
                    ),
                    css_class="form-row",
                )
        )

class AlerceBroker(GenericBroker):
    # name = 'ALeRCE'
    # form = AlerceQueryForm

    def _fetch_alerts_payload(self, parameters):
        payload = {
            'page': parameters.get('page', 1),
            'query_parameters': {
            }
        }

        if any([parameters['nobs__gt'], parameters['nobs__lt'], parameters['classrf'], parameters['pclassrf']]):
            filters = {}
            if any([parameters['nobs__gt'], parameters['nobs__lt']]):
                filters['nobs'] = {}
                if parameters['nobs__gt']:
                    filters['nobs']['min'] = parameters['nobs__gt']
                if parameters['nobs__lt']:
                    filters['nobs']['max'] = parameters['nobs__lt']
            if parameters['classrf']:
                filters['classrf'] = parameters['classrf']
            if parameters['pclassrf']:
                filters['pclassrf'] = parameters['pclassrf']
            if parameters['classearly']:
                filters['classearly'] = parameters['classearly']
            if parameters['pclassearly']:
                filters['pclassearly'] = parameters['pclassearly']
            payload['query_parameters']['filters'] = filters

        if any([parameters['ra'], parameters['dec'], parameters['sr']]):
            coordinates = {}
            if parameters['ra']:
                coordinates['ra'] = parameters['ra']
            if parameters['dec']:
                coordinates['dec'] = parameters['dec']
            if parameters['sr']:
                coordinates['sr'] = parameters['sr']
            payload['query_parameters']['coordinates'] = coordinates

        if any([parameters['mjd__gt'], parameters['mjd__lt']]):
            dates = {'firstmjd': {}}
            if parameters['mjd__gt']:
                dates['firstmjd']['min'] = parameters['mjd__gt']
            if parameters['mjd__lt']:
                dates['firstmjd']['max'] = parameters['mjd__lt']
            payload['query_parameters']['dates'] = dates

        return payload
