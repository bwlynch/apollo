import logging
from lxml import etree
from django.db import transaction
import tabimport
from unidecode import unidecode
from .models import Form, LocationType, Location, Edge, Observer, ObserverRole, Submission


logger = logging.getLogger(__name__)


@transaction.commit_manually
def import_forms(source):
    tree = etree.HTML(source)
    forms = tree.xpath('//form')
    for form in forms:
        try:
            try:
                _form = Form.objects.get(name=form.attrib.get('name'))

                # update form parameters
                _form.type = form.attrib.get('data-type').upper()
                _form.trigger = form.attrib.get('data-trigger')
                _form.field_pattern = form.attrib.get('data-field_pattern')
                if _form.type == 'INCIDENT':
                    _form.autocreate_submission = True
                else:
                    _form.autocreate_submission = False
                _form.save()
            except Form.DoesNotExist:
                # create the form
                _form = Form.objects.create(name=form.attrib.get('name'),
                    type=form.attrib.get('data-type').upper(),
                    trigger=form.attrib.get('data-trigger'),
                    field_pattern=form.attrib.get('data-field_pattern'),
                    autocreate_submission=True
                        if form.attrib.get('data-type').upper() == 'INCIDENT' else False)

            # delete existing groups
            _form.groups.all().delete()
            fieldsets = form.xpath('descendant::fieldset')
            for fieldset in fieldsets:
                try:
                    legend = fieldset.xpath('descendant::legend')[0]
                except IndexError:
                    raise SyntaxError('form fieldsets must specify a legend')

                # create form group
                _group = _form.groups.create(name=legend.text,
                    abbr=fieldset.attrib.get('name', ''))

                # delete existing fields
                _group.fields.all().delete()
                fields = fieldset.xpath('descendant::input|descendant::select')
                for field in fields:
                    # create the field
                    _field = _group.fields.create(name=field.attrib.get('name'),
                        tag=field.attrib.get('name'),
                        description=field.attrib.get('title', ''))

                    # the remaining configuration is dependent on the type of the field
                    if field.tag == 'input':
                        if field.attrib.get('type') == 'checkbox':
                            _field.present_true = True
                        else:
                            if field.attrib.get('min', None):
                                _field.lower_limit = field.attrib.get('min')
                            if field.attrib.get('max', None):
                                _field.upper_limit = field.attrib.get('max')
                    elif field.tag == 'select':
                        if 'multiple' in field.attrib:
                            _field.allow_multiple = True

                        # if there are any field options, delete them
                        _field.options.all().delete()
                        options = field.xpath('descendant::option')
                        for option in options:
                            # create the field option
                            _field.options.create(option=option.attrib.get('value'),
                                description=option.text)

                    _field.save()
        except Exception, e:
            transaction.rollback()
            raise e
        transaction.commit()


@transaction.commit_manually
def import_location_types(source, flush=False):
    try:
        if flush:
            LocationType.objects.all().delete()
        tree = etree.XML(source)
        for lt in tree.getchildren():
            process_location_type(lt)
        transaction.commit()
    except Exception, e:
        transaction.rollback()
        raise e


def process_location_type(location_type):
    lt, _ = LocationType.objects.get_or_create(name=location_type.attrib.get('name'))
    parent = location_type.getparent()
    if parent.tag == 'location':
        # link the parent to the location_type
        lt_parent = LocationType.objects.get(name=parent.attrib.get('name'))
        lt.add_parent(lt_parent)
    else:
        # if it doesn't have any defined parents, then delete any linked
        # parents if any exist
        Edge.objects.filter(node_from=lt.node(graph=lt.default_graph)).delete()
    for child in location_type.getchildren():
        process_location_type(child)


@transaction.commit_manually
def import_locations(filename, mapping):
    def get_line_value(line, key):
        if callable(key):
            value = key(line)
            # only transliterate unicode or str objects
            if type(value) in [unicode, str]:
                return unidecode(unicode(value))
            else:
                return value
        elif key is None or key == '':
            return key
        else:
            return unidecode(unicode(line.get(key))).strip()

    def set_location_attributes(location, attributes, line, mapping):
        for attribute in attributes:
            value = get_line_value(line, mapping[attribute])
            pk, attr = attribute.split('__')
            setattr(location, attr, value)

    def set_location_parents(location, locations, location_type_id, location_type_ids):
        parent_ids = map(lambda locationtype: str(locationtype.pk),
            location_type_ids[location_type_id].get_parents())
        if parent_ids:
            for parent_id in parent_ids:
                location.add_parent(locations[parent_id])

    imported = tabimport.FileFactory(filename)
    map_keys = mapping.keys()
    location_types = LocationType.root().get_descendants(include_self=True)
    location_type_ids = map(lambda lt: str(lt.pk), location_types)
    location_types_hash = {}
    for lt in location_types:
        location_types_hash[str(lt.pk)] = lt

    try:
        for line in imported:
            line_locations = {}  # locations extracted from the line are stored here for reuse
            for location_type_id in location_type_ids:
                lt_mapping = filter(lambda k: k.startswith(location_type_id), map_keys)
                if lt_mapping:
                    location, _ = Location.objects.get_or_create(
                        name=get_line_value(line, mapping['{}__name'.format(location_type_id)]),
                        type=location_types_hash[location_type_id],
                        code=get_line_value(line, mapping['{}__code'.format(location_type_id)]))
                    set_location_attributes(location, lt_mapping, line, mapping)
                    set_location_parents(location, line_locations, location_type_id, location_types_hash)
                    location.save()
                    logger.debug('Saved: {} - {}'.format(location.type.name, location.name))

                    # save location for later retrieval
                    line_locations[location_type_id] = location
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise


@transaction.commit_manually
def import_observers(filename, mapping):
    def get_line_value(line, key):
        if callable(key):
            value = key(line)
            # only transliterate unicode or str objects
            if type(value) in [unicode, str]:
                return unidecode(unicode(value))
            else:
                return value
        else:
            return unidecode(unicode(line.get(key))).strip()

    def set_observer_attributes(observer, line, mapping):
        # phone numbers are saved differently
        for attribute in filter(lambda k: k != 'phone', mapping.keys()):
            value = get_line_value(line, mapping[attribute])
            setattr(observer, attribute, value)

    imported = tabimport.FileFactory(filename)
    try:
        for line in imported:
            logger.debug('Creating/Updating Observer: {}'.format(mapping['observer_id']))
            try:
                observer = Observer.objects.get(observer_id=get_line_value(line, mapping['observer_id']))
            except Observer.DoesNotExist:
                observer = Observer()
            set_observer_attributes(observer, line, mapping)
            observer.save()

            # set the phone number again in-case the observer was just created
            if 'phone' in mapping.keys():
                observer.phone = get_line_value(line, mapping['phone'])
                observer.save()
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise


def create_checklists(form, role, date):
    if type(role) == str:
        role = ObserverRole.objects.get(name=role)
    if type(form) == str:
        form = Form.objects.get(name=form)

    observers = Observer.objects.filter(role=role)
    for observer in observers:
        Submission.objects.get_or_create(form=form,
            observer=observer, location=observer.location,
            date=date)