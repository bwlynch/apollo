from webapp.api import *
from webapp.models import *
from models import *
from django.db.models import Q

class ChecklistResponseResource(ModelResource):    
    class Meta:
        queryset = ZambiaChecklistResponse.objects.select_related()
        resource_name = 'checklist_response'
        allowed_methods = ['get', 'put', 'post', 'delete']
        authentication = Authentication()
        authorization = Authorization()


class ChecklistResource(ModelResource):
    location = fields.ForeignKey(LocationResource, 'location', full=True)
    observer = fields.ForeignKey(ContactResource, 'observer', full=True)
    response = fields.ToOneField(ChecklistResponseResource, 'response', full=True)

    class Meta:
        queryset = Checklist.objects.select_related()
        resource_name = 'checklist'
        allowed_methods = ['get', 'put', 'post', 'delete']
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            'date': ALL,
            'response': ALL_WITH_RELATIONS,
            'observer': ALL_WITH_RELATIONS,
            'location': ALL_WITH_RELATIONS,
        }
        ordering = ['location', 'date', 'observer']

    def build_filters(self, filters=None):
        if not filters:
            filters = {}

        orm_filters = super(ChecklistResource, self).build_filters(filters)
        
        if orm_filters.has_key('location__id__exact'):
            id = orm_filters.pop('location__id__exact')
            orm_filters['location__id__in'] = Location.objects.get(id=id).get_descendants(True).values_list('id', flat=True)
        
        if 'setup_status' in filters:
            status = filters.get('setup_status')
            if status == '1': # complete
                orm_filters.update(dict([('response__%s__isnull' % field, False) for field in \
                    ['A', 'B', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'D', 'E', 'EA', \
                    'EB', 'EC', 'F', 'G', 'H', 'J']]))
                
            elif status == '2': # missing
                orm_filters.update(dict([('response__%s__isnull' % field, True) for field in \
                    ['A', 'B', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'D', 'E', 'EA', \
                    'EB', 'EC', 'F', 'G', 'H', 'J']]))
                    
            elif status == '3': # partial
                query = None
                complete_query = None
                for field in ['A', 'B', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'D', \
                    'E', 'EA', 'EB', 'EC', 'F', 'G', 'H', 'J']:
                    if not query:
                        exec 'query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'query |= Q(response__%s__isnull=False)' % field
                    if not complete_query:
                        exec 'complete_query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'complete_query &= Q(response__%s__isnull=False)' % field
                exec 'query &= ~(complete_query)'
                orm_filters['pk__in'] = Checklist.objects.filter(query).values_list('id', flat=True)

        if 'voting_status' in filters:
            status = filters.get('voting_status')
            if status == '1': # complete
                orm_filters.update(dict([('response__%s__isnull' % field, False) for field in \
                    ['K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']]))
                
            elif status == '2': # missing
                orm_filters.update(dict([('response__%s__isnull' % field, True) for field in \
                    ['K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']]))
                    
            elif status == '3': # partial
                query = None
                complete_query = None
                for field in ['K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']:
                    if not query:
                        exec 'query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'query |= Q(response__%s__isnull=False)' % field
                    if not complete_query:
                        exec 'complete_query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'complete_query &= Q(response__%s__isnull=False)' % field
                exec 'query &= ~(complete_query)'
                orm_filters['pk__in'] = Checklist.objects.filter(query).values_list('id', flat=True)

        if 'closing_status' in filters:
            status = filters.get('closing_status')
            if status == '1': # complete
                orm_filters.update(dict([('response__%s__isnull' % field, False) for field in \
                    ['X', 'Y', 'Z', 'AA']]))
                    
            elif status == '2': # missing
                orm_filters.update(dict([('response__%s__isnull' % field, True) for field in \
                    ['X', 'Y', 'Z', 'AA']]))
                    
            elif status == '3': # partial
                query = None
                complete_query = None
                for field in ['X', 'Y', 'Z', 'AA']:
                    if not query:
                        exec 'query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'query |= Q(response__%s__isnull=False)' % field
                    if not complete_query:
                        exec 'complete_query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'complete_query &= Q(response__%s__isnull=False)' % field
                exec 'query &= ~(complete_query)'
                orm_filters['pk__in'] = Checklist.objects.filter(query).values_list('id', flat=True)

        if 'counting_status' in filters:
            status = filters.get('counting_status')
            if status == '1': # complete
                orm_filters.update(dict([('response__%s__isnull' % field, False) for field in \
                    ['AB', 'AC', 'AD', 'AEAA', 'AEAB', 'AEAC', 'AEAD', 'AEAE', 'AEAF', 'AEBA', 'AEBB', 'AEBC', \
                    'AEBD', 'AEBE', 'AEBF', 'AECA', 'AECB', 'AECC', 'AECD', 'AECE', 'AECF', 'AEDA', 'AEDB', \
                    'AEDC', 'AEDD', 'AEDE', 'AEDF', 'AEEA', 'AEEB', 'AEEC', 'AEED', 'AEEE', 'AEEF', 'AFAA', \
                    'AFAB', 'AFAC', 'AFAD', 'AFAE', 'AFAF', 'AFBA', 'AFBB', 'AFBC', 'AFBD', 'AFBE', 'AFBF', \
                    'AG', 'AH', 'AJ', 'AK']]))
                    
            elif status == '2': # missing
                orm_filters.update(dict([('response__%s__isnull' % field, True) for field in \
                    ['AB', 'AC', 'AD', 'AEAA', 'AEAB', 'AEAC', 'AEAD', 'AEAE', 'AEAF', 'AEBA', 'AEBB', 'AEBC', \
                    'AEBD', 'AEBE', 'AEBF', 'AECA', 'AECB', 'AECC', 'AECD', 'AECE', 'AECF', 'AEDA', 'AEDB', \
                    'AEDC', 'AEDD', 'AEDE', 'AEDF', 'AEEA', 'AEEB', 'AEEC', 'AEED', 'AEEE', 'AEEF', 'AFAA', \
                    'AFAB', 'AFAC', 'AFAD', 'AFAE', 'AFAF', 'AFBA', 'AFBB', 'AFBC', 'AFBD', 'AFBE', 'AFBF', \
                    'AG', 'AH', 'AJ', 'AK']]))
                    
            elif status == '3': # partial
                query = None
                complete_query = None
                for field in ['AB', 'AC', 'AD', 'AEAA', 'AEAB', 'AEAC', 'AEAD', 'AEAE', 'AEAF', 'AEBA', 'AEBB', 'AEBC', \
                'AEBD', 'AEBE', 'AEBF', 'AECA', 'AECB', 'AECC', 'AECD', 'AECE', 'AECF', 'AEDA', 'AEDB', \
                'AEDC', 'AEDD', 'AEDE', 'AEDF', 'AEEA', 'AEEB', 'AEEC', 'AEED', 'AEEE', 'AEEF', 'AFAA', \
                'AFAB', 'AFAC', 'AFAD', 'AFAE', 'AFAF', 'AFBA', 'AFBB', 'AFBC', 'AFBD', 'AFBE', 'AFBF', \
                'AG', 'AH', 'AJ', 'AK']:
                    if not query:
                        exec 'query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'query |= Q(response__%s__isnull=False)' % field
                    if not complete_query:
                        exec 'complete_query = Q(response__%s__isnull=False)' % field
                    else:
                        exec 'complete_query &= Q(response__%s__isnull=False)' % field
                exec 'query &= ~(complete_query)'
                orm_filters['pk__in'] = Checklist.objects.filter(query).values_list('id', flat=True)

        return orm_filters


class IncidentResponseResource(ModelResource):    
    class Meta:
        queryset = ZambiaIncidentResponse.objects.select_related()
        resource_name = 'incident_response'
        allowed_methods = ['get', 'put', 'post', 'delete']
        authentication = Authentication()
        authorization = Authorization()


class IncidentResource(ModelResource):
    location = fields.ForeignKey(LocationResource, 'location', full=True)
    observer = fields.ForeignKey(ContactResource, 'observer', full=True)
    response = fields.ToOneField(IncidentResponseResource, 'response', full=True)
    
    class Meta:
        queryset = Incident.objects.select_related()
        resource_name = 'incident'
        allowed_methods = ['get', 'put', 'post', 'delete']
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            'date': ALL,
            'observer': ALL_WITH_RELATIONS,
            'location': ALL_WITH_RELATIONS,
            'response': ALL_WITH_RELATIONS,
        }
        ordering = ['location', 'date', 'observer']
