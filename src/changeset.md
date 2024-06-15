# file: /home/r/ws/sag/src/psy/apps/base/values.py
```python
PFA_ONLINE_PRODUCTS = {
    PFA_ONLINE_PSYKOLOGI: {
        "id": PFA_ONLINE_PSYKOLOGI,
        "pfa_uuid": "HSD0072",
        "title": "Online Psykolog",
        "resource_title": "psykolog",
        "resource_title_definite": "psykologen",
        "slug": "pfa-online-psykolog",
        "default_case_kwargs": DEFAULT_CASE_KWARGS_FOR_NEW_ONLINE_PRODUCTS_CASE,
        "show_acute_info": True,
        "child_age_min": 12,
        "child_age_max": 24,
        "cancellation_fee": 975,
        "new_guy!": 1234,
    },
    PFA_ONLINE_COACH: {
        "id": PFA_ONLINE_COACH,
        "pfa_uuid": "HSD0073",
        "title": "Online Coach",
        "resource_title": "coach",
        "resource_title_definite": "coachen",
        "slug": "pfa-online-coach",
        "default_case_kwargs": DEFAULT_CASE_KWARGS_FOR_NEW_ONLINE_PRODUCTS_CASE,
        "show_acute_info": False,
        "child_age_min": 15,
        "child_age_max": 24,
        "cancellation_fee": 850,
        "alsogood!": 9999,
    },
    PFA_ONLINE_FAMILIE: {
        "id": PFA_ONLINE_FAMILIE,
        "pfa_uuid": "HSD0074",
        "title": "Online Familierådgiver",
        "resource_title": "familierådgiver",
        "resource_title_definite": "familierådgiveren",
        "slug": "pfa-online-familieraadgiver",
        "default_case_kwargs": DEFAULT_CASE_KWARGS_FOR_NEW_ONLINE_PRODUCTS_CASE,
        "show_acute_info": False,
        "cancellation_fee": 850,
    },
}
```

# file: /home/r/ws/sag/src/psy/apps/counseling/models.py
```python
class ResourcePhonecall(ModelBase):
    """
    A ResourcePhoneCall represents a phonecall made by a counselor to
    a Resource regarding a specific case.

    CODE
    """

    resource = m.ForeignKey('staff.Resource', verbose_name="Konsulent", on_delete=m.PROTECT)

    case = m.ForeignKey('Case', verbose_name='Sag', on_delete=m.CASCADE)
    # what was the call about? Will be listed in journal entryies
    note = m.CharField('Note', max_length=80, blank=True)

    class Meta:
        verbose_name = 'Konsulentopringning'
        verbose_name_plural = 'Konsulentopringninger'
        guys = 1234

    def clean(self, *args, **kwargs):
        if self.case_id is not None:
            validate_resource_against_related(self.case, self, validate_related_has_health_insurance=False)
        return super(ResourcePhonecall, self).clean(*args, **kwargs)
```

# file: /home/r/ws/sag/src/psy/apps/help/appointments/api.py
```python
def consultations_data_new_cases(request):
    client = client_from_user(request.user)
    case_has_timeslot = CaseHour.objects.filter(case=OuterRef('pk'), timeslot__isnull=False)
    this_is_great!

    return Case.objects.filter(
        client=client, coverage__online_product__isnull=False, casestatus_id=CASESTATUS_ACTIVE_ID,
        track_a_case_client_procedure__status=ClientProcedure.STATUS().OPEN.id).annotate(
            has_timeslot=Exists(case_has_timeslot)).filter(Q(casehour__isnull=True) | Q(has_timeslot=False))
```
