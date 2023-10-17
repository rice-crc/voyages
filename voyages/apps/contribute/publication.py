from __future__ import absolute_import, unicode_literals
import json

import os
import re
import traceback
from builtins import str
from itertools import chain

import requests
from django.conf import settings
from django.core import management
from django.db import transaction
import unicodecsv as csv

from voyages.apps.common.models import year_mod
from voyages.apps.common.utils import get_multi_valued_column_suffix
from voyages.apps.contribute.models import (ContributionStatus,
                                            DeleteVoyageContribution,
                                            EditVoyageContribution,
                                            InterimPreExistingSourceActions,
                                            MergeVoyagesContribution,
                                            NewVoyageContribution,
                                            ReviewRequest,
                                            ReviewRequestDecision)
from voyages.apps.past.models import VoyageCaptainOwnerHelper
from voyages.apps.voyage.models import (Voyage,
                                        VoyageCargoConnection, VoyageCrew,
                                        VoyageDates,
                                        VoyageItinerary, VoyageOutcome,
                                        VoyagesFullQueryHelper, VoyageShip,
                                        VoyageSlavesNumbers, VoyageSources,
                                        VoyageSourcesConnection)

if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE <= 2:
    from voyages.apps.voyage.models import (VoyageCaptain, VoyageCaptainConnection, VoyageShipOwner, VoyageShipOwnerConnection)

CARGO_COLUMN_COUNT = 10

_exported_spss_fields = [
    'VOYAGEID', 'STATUS', 'ADLT1IMP', 'ADLT2IMP', 'ADLT3IMP', 'ADPSALE1',
    'ADPSALE2', 'ADULT1', 'ADULT2', 'ADULT3', 'ADULT4', 'ADULT5', 'ADULT6',
    'ADULT7', 'ARRPORT', 'ARRPORT2', 'ARRPORT3', 'ARRPORT4', 'BOY1', 'BOY2', 'BOY3', 'BOY4', 'BOY5',
    'BOY6', 'BOY7', 'BOYRAT7', 'CAPTAINA', 'CAPTAINB', 'CAPTAINC', 'CHIL1IMP',
    'CHIL2IMP', 'CHIL3IMP', 'CHILD1', 'CHILD2', 'CHILD3', 'CHILD4', 'CHILD5',
    'CHILD6', 'CHILD7', 'CHILRAT7', 'CONSTREG', 'CREW', 'CREW1', 'CREW2',
    'CREW3', 'CREW4', 'CREW5', 'CREWDIED', 'DATEDEPA', 'DATEDEPB', 'DATEDEPC',
    'D1SLATRA', 'D1SLATRB', 'D1SLATRC', 'DLSLATRA', 'DLSLATRB', 'DLSLATRC',
    'DDEPAM', 'DDEPAMB', 'DDEPAMC', 'DATARR32', 'DATARR33', 'DATARR34',
    'DATARR36', 'DATARR37', 'DATARR38', 'DATARR39', 'DATARR40', 'DATARR41',
    'DATARR43', 'DATARR44', 'DATARR45', 'DATEDEP', 'DATEBUY', 'DATELEFTAFR',
    'DATELAND1', 'DATELAND2', 'DATELAND3', 'DATEDEPAM', 'DATEEND',
    'DEPTREGIMP', 'DEPTREGIMP1', 'EMBPORT', 'EMBPORT2', 'EMBREG', 'EMBREG2',
    'EVGREEN', 'FATE', 'FATE2', 'FATE3', 'FATE4', 'FEMALE1', 'FEMALE2',
    'FEMALE3', 'FEMALE4', 'FEMALE5', 'FEMALE6', 'FEMALE7', 'FEML1IMP',
    'FEML2IMP', 'FEML3IMP', 'GIRL1', 'GIRL2', 'GIRL3', 'GIRL4', 'GIRL5',
    'GIRL6', 'GIRL7', 'GIRLRAT7', 'GUNS', 'INFANT1', 'INFANT2', 'INFANT3',
    'INFANT4', 'INFANT5', 'INFANT6', 'JAMCASPR', 'MAJBUYPT', 'MAJBYIMP',
    'MAJBYIMP1', 'MAJSELPT', 'MALE1', 'MALE1IMP', 'MALE2', 'MALE2IMP', 'MALE3',
    'MALE3IMP', 'MALE4', 'MALE5', 'MALE6', 'MALE7', 'MALRAT7', 'MEN1', 'MEN2',
    'MEN3', 'MEN4', 'MEN5', 'MEN6', 'MEN7', 'MENRAT7', 'MJBYPTIMP', 'MJSELIMP',
    'MJSELIMP1', 'MJSLPTIMP', 'NATINIMP', 'NATIONAL', 'NCAR13', 'NCAR15',
    'NCAR17', 'NDESERT', 'NPAFTTRA', 'NPPRETRA', 'NPPRIOR', 'OWNERA', 'OWNERB',
    'OWNERC', 'OWNERD', 'OWNERE', 'OWNERF', 'OWNERG', 'OWNERH', 'OWNERI',
    'OWNERJ', 'OWNERK', 'OWNERL', 'OWNERM', 'OWNERN', 'OWNERO', 'OWNERP',
    'PLAC1TRA', 'PLAC2TRA', 'PLAC3TRA', 'PLACCONS', 'PLACREG', 'PORTDEP',
    'PORTRET', 'PTDEPIMP', 'REGARR', 'REGARR2', 'REGARR3', 'REGARR4', 'REGDIS1', 'REGDIS2',
    'REGDIS3', 'REGEM1', 'REGEM2', 'REGEM3', 'REGISREG', 'RESISTANCE',
    'RETRNREG', 'RETRNREG1', 'RIG', 'SAILD1', 'SAILD2', 'SAILD3', 'SAILD4',
    'SAILD5', 'SHIPNAME', 'SLA1PORT', 'SLAARRIV', 'SLADAFRI', 'SLADAMER',
    'SLADVOY', 'SLAMIMP', 'SLAS32', 'SLAS36', 'SLAS39', 'SLAVEMA1', 'SLAVEMA3',
    'SLAVEMA7', 'SLAVEMX1', 'SLAVEMX3', 'SLAVEMX7', 'SLAVMAX1', 'SLAVMAX3',
    'SLAVMAX7', 'SLAXIMP', 'SLINTEN2', 'SLINTEND', 'SOURCEA', 'SOURCEB',
    'SOURCEC', 'SOURCED', 'SOURCEE', 'SOURCEF', 'SOURCEG', 'SOURCEH',
    'SOURCEI', 'SOURCEJ', 'SOURCEK', 'SOURCEL', 'SOURCEM', 'SOURCEN',
    'SOURCEO', 'SOURCEP', 'SOURCEQ', 'SOURCER', 'TONMOD', 'TONNAGE', 'TONTYPE',
    'TSLAVESD', 'TSLAVESP', 'TSLMTIMP', 'VOY1IMP', 'VOY2IMP', 'VOYAGE',
    'VYMRTIMP', 'VYMRTRAT', 'WOMEN1', 'WOMEN2', 'WOMEN3', 'WOMEN4', 'WOMEN5',
    'WOMEN6', 'WOMEN7', 'WOMRAT7', 'XMIMPFLAG', 'YEAR10', 'YEAR100', 'YEAR25',
    'YEAR5', 'YEARAF', 'YEARAM', 'YEARDEP', 'YRCONS', 'YRREG', 'VOYAGEID2',
    'DATASET', "BOYRAT1", "CHILRAT1", "GIRLRAT1", "MALRAT1", "MENRAT1",
    "WOMRAT1", "BOYRAT3", "CHILRAT3", "GIRLRAT3", "MALRAT3", "MENRAT3",
    "WOMRAT3", "COMMENTS"
] + \
["CARGOTYPE" + suffix for suffix in get_multi_valued_column_suffix(CARGO_COLUMN_COUNT, True)] + \
["CARGOUNIT" + suffix for suffix in get_multi_valued_column_suffix(CARGO_COLUMN_COUNT, True)] + \
["CARGOAMOUNT" + suffix for suffix in get_multi_valued_column_suffix(CARGO_COLUMN_COUNT, True)] + \
["AFRINFO" + suffix for suffix in get_multi_valued_column_suffix(3, True)]

# TODO: Some variables are not an exact match to any field in or models,
# so they either have some correspondence with a computed value from those
# fields, or they are deprecated. E.g *RAT1, *RAT3 fields.


def get_header_csv_text():
    return ','.join(_exported_spss_fields) + '\n'


def get_csv_writer(output):
    return csv.DictWriter(output, fieldnames=_exported_spss_fields)


def safe_writerow(writer, item):
    """
    Ensure that only "export SPSS fields" are included in the item that will be
    written.
    """
    safe = {
        k: v for (k, v) in [
            (field, item.get(field))
            for field in _exported_spss_fields
        ] if v is not None
    }
    return writer.writerow(safe)


def _get_interim_additional_ship_owners(interim):
    if not interim.additional_ship_owners:
        return []
    additional = [
        re.sub('[\r\n]', '', x)
        for x in interim.additional_ship_owners.split('\n')
    ]
    return [x for x in additional if len(x) > 0]


def export_contributions(statuses):
    """
    Produce a list of dicts, each representing a contribution.
    """
    (review_requests, notreviewed) = _fetch_active_reviews_by_status(statuses)
    for data in export_from_review_requests(review_requests):
        yield data
    for user_contrib in notreviewed:
        for data in export_contribution(user_contrib, None, None,
                                        'not reviewed'):
            yield data


def export_from_review_requests(review_requests):
    for req in review_requests:
        contrib = req.editor_contribution.first()
        user_contribution = req.contribution()
        status_text = 'undecided'
        if req.final_decision == ReviewRequestDecision.accepted_by_editor:
            status_text = 'accepted by editor'
        elif req.final_decision == ReviewRequestDecision.rejected_by_editor:
            status_text = 'rejected by editor'
        items = export_contribution(
            user_contribution,
            (contrib.interim_voyage
             if hasattr(contrib, 'interim_voyage') else None),
            (req.created_voyage_id
             if req.requires_created_voyage_id() else None),
            status_text, req.dataset)
        for data in items:
            yield data


def export_contribution(user_contrib,
                        interim_voyage,
                        created_voyage_id,
                        status_text,
                        dataset=0):
    if isinstance(user_contrib, DeleteVoyageContribution):
        delete_ids = user_contrib.deleted_voyages_ids.split(',')
        voyages = Voyage.all_dataset_objects.filter(voyage_id__in=delete_ids)
        for v in voyages:
            data = _map_voyage_to_spss(v)
            data['STATUS'] = 'DELETE (%s)' % status_text
            yield data
        return
    if interim_voyage is None:
        interim_voyage = user_contrib.interim_voyage
    if interim_voyage is None:
        return
    data = _map_interim_to_spss(interim_voyage)
    ids = user_contrib.get_related_voyage_ids()
    if created_voyage_id:
        data['VOYAGEID'] = created_voyage_id
    else:
        data['VOYAGEID'] = ' '.join([str(id) for id in ids])
    data['DATASET'] = dataset
    if isinstance(user_contrib, NewVoyageContribution):
        data['STATUS'] = 'NEW (%s)' % status_text
    elif isinstance(user_contrib, EditVoyageContribution):
        data['STATUS'] = 'EDIT (%s)' % status_text
    elif isinstance(user_contrib, MergeVoyagesContribution):
        data['STATUS'] = 'MERGE of %s (%s)' % (', '.join(
            [str(id) for id in ids]), status_text)
    else:
        data['STATUS'] = 'UNKNOW CONTRIBUTION TYPE (%s)' % status_text
    yield data


def export_from_voyages(dataset=None):
    helper = VoyagesFullQueryHelper()
    voyages = helper.get_query(dataset)
    # To speed up performance and memory usage we first
    # fetch the ids and peform windowed queries.
    ids = sorted(helper.get_manager(dataset).values_list('pk', flat=True))
    row_start = 0
    while row_start < len(ids):
        row_end = row_start + 1000
        if row_end > len(ids):
            row_end = len(ids)
        page = voyages.filter(pk__gte=ids[row_start], pk__lte=ids[row_end - 1])
        for v in page:
            yield _map_voyage_to_spss(v)
        row_start = row_end
    voyages.prefetch_related(None)
    voyages = None


def publish_accepted_contributions(log_file, skip_backup=False):
    """
    Publish all accepted contributions and use the
    given log_file to register the progress. Since
    all the db operations are transacional, either
    everything is published or nothing is.
    """
    def log(text):
        log_file.write(text)
        log_file.flush()
        os.fsync(log_file.fileno())

    transaction_finished = False
    transaction_started = False
    try:
        # Step 1 - Backup database
        if not skip_backup:
            log('Backing up all data.\n')
            with open(settings.MEDIA_ROOT + '/db.json', 'w') as f:
                management.call_command('dumpdata', stdout=f)
            log('Finished backup.\n')

        log('Fetching contributions...\n')
        (review_requests,
         _) = _fetch_active_reviews_by_status([ContributionStatus.approved])
        log('Publishing...\n')
        # Step 2 - Publish database
        all_deleted_ids = []
        transaction_started = True
        with transaction.atomic():
            count = 0
            for req in review_requests:
                # Basic validation.
                count += 1
                log('Processing ' + req.contribution_id + '\n')
                if req.final_decision != (
                        ReviewRequestDecision.accepted_by_editor):
                    raise Exception(
                        'Review cannot be published since it was not accepted '
                        'by editor'
                    )
                if req.contribution_id.startswith('delete'):
                    _publish_single_review_delete(req, all_deleted_ids)
                elif req.contribution_id.startswith('merge'):
                    _publish_single_review_merge(req, all_deleted_ids)
                elif req.contribution_id.startswith('new'):
                    _publish_single_review_new(req)
                elif req.contribution_id.startswith('edit'):
                    _publish_single_review_update(req)
                else:
                    raise Exception('Unexpected contribution type')
                contribution = req.contribution()
                contribution.status = ContributionStatus.published
                contribution.save()
                req.archived = True
                req.save()
        transaction_finished = True
        log('Finished all publications.\n')
        log('Total published: ' + str(count) + '.\n')
        # Step 3 - Update solr index.
        log('Updating solr index.\n')
        # Take care of deleted documents first.
        try:
            entry = settings.HAYSTACK_CONNECTIONS.get('default')
            solr_url = entry.get('URL') if entry else None
            if solr_url:
                solr_url += '/update'
                headers = {'Content-type': 'text/xml'}

                def post(data):
                    return requests.post(solr_url, data, headers=headers)

                def post_delete_request(voyage_id):
                    r = post('<delete><query>'
                             f'var_voyage_id:{voyage_id}</query></delete>')
                    if r.status_code != 200:
                        log('Failed to delete Solr record for '
                            'voyage_id ' + str(voyage_id) + ' '
                            'response code: ' + str(r.status_code))
                        return
                    r = post('<commit />')
                    if r.status_code != 200:
                        log('Failed to commit deletion for Solr record for '
                            'voyage_id ' + str(voyage_id) + ' '
                            'response code: ' + str(r.status_code))

                for voyage_id in all_deleted_ids:
                    post_delete_request(voyage_id)
        except Exception:
            pass
        management.call_command('update_index',
                                'voyage.voyage',
                                age=24,
                                stdout=log_file)
        log('Solr index is now updated.\n')
        return True
    except Exception as exception:
        log('An error occurred.\n')
        if transaction_started and not transaction_finished:
            transaction.rollback()
            log('Database transaction was rolledback.\n')
        log(str(exception))
        log(traceback.format_exc())
        return False
    finally:
        log('EOF')
        log_file.close()


def _delete_child_fk(obj, child_attr):
    child = getattr(obj, child_attr)
    if child:
        setattr(obj, child_attr, None)
        obj.save()
        child.delete()


def full_contribution_id(contribution_type, contribution_id):
    return contribution_type + '/' + str(contribution_id)


def get_contrib_default_query(model):
    return model.objects.select_related('contributor')


def get_filtered_contributions(filter_args):
    all_types = [
        [{
            'type': name,
            'id': x.pk,
            'contribution': x
        } for x in get_contrib_default_query(contrib).filter(**filter_args)]
        for name, contrib
        in [('edit', EditVoyageContribution),
            ('merge', MergeVoyagesContribution),
            ('delete', DeleteVoyageContribution),
            ('new', NewVoyageContribution)]
    ]
    return sum(all_types, [])


def _fetch_active_reviews_by_status(statuses):
    contribution_info = get_filtered_contributions({'status__in': statuses})
    review_requests = []
    notreviewed_contributions = []
    for info in contribution_info:
        contrib_id = full_contribution_id(info['type'], info['id'])
        reqs = list(
            ReviewRequest.objects.filter(contribution_id=contrib_id,
                                         archived=False))
        if len(reqs) != 1 and info[
                'contribution'].status == ContributionStatus.approved:
            raise Exception(
                'Expected a single active review request for approved '
                'contributions [' + str(contrib_id) + '], '
                'found: ' + str(len(reqs)))
        if len(reqs) == 0:
            notreviewed_contributions.append(info['contribution'])
        else:
            review_requests += reqs
    return review_requests, notreviewed_contributions


def _map_csv_date(data, varname, csv_date, labels=None):
    if csv_date is None:
        return
    members = csv_date.split(',')
    if len(members) != 3:
        members = [None, None, None]
    if labels is None:
        labels = ['A', 'B', 'C']
    data[varname + labels[0]] = int(
        members[1]) if members[1] and members[1] != '' else None
    data[varname + labels[1]] = int(
        members[0]) if members[0] and members[0] != '' else None
    data[varname + labels[2]] = int(
        members[2]) if members[2] and members[2] != '' else None


def _get_label_value(x):
    return x.value if x else None


def _get_region_value(place):
    return place.region.value if place else None

_captain_owner_helper = VoyageCaptainOwnerHelper()

def _map_voyage_to_spss(voyage):
    data = {'STATUS': 'PUBLISHED'}
    data['VOYAGEID'] = voyage.voyage_id
    data['DATASET'] = voyage.dataset

    # Dates
    def sanitize_date(csv_date):
        return csv_date if csv_date != ',,' else ''

    dates = voyage.voyage_dates
    data['DATEDEP'] = sanitize_date(dates.voyage_began) if dates else None
    data['DATEEND'] = sanitize_date(dates.voyage_completed) if dates else None
    data['DATEBUY'] = sanitize_date(dates.slave_purchase_began) if dates else None
    data['DATELEFTAFR'] = sanitize_date(dates.date_departed_africa) if dates else None
    data['DATELAND1'] = sanitize_date(dates.first_dis_of_slaves) if dates else None
    data['DATELAND2'] = sanitize_date(dates.arrival_at_second_place_landing) if dates else None
    data['DATELAND3'] = sanitize_date(dates.third_dis_of_slaves) if dates else None
    data['DATEDEPAM'] = sanitize_date(dates.departure_last_place_of_landing) if dates else None
    _map_csv_date(data, 'DATEDEP', dates.voyage_began if dates else None)
    _map_csv_date(data, 'D1SLATR', dates.slave_purchase_began if dates else None)
    _map_csv_date(data, 'DLSLATR', dates.vessel_left_port if dates else None)
    _map_csv_date(data, 'DATARR3', dates.first_dis_of_slaves if dates else None, '234')
    _map_csv_date(data, 'DATARR3',
                  dates.arrival_at_second_place_landing if dates else None, '678')
    _map_csv_date(data, 'DATARR', dates.third_dis_of_slaves if dates else None,
                  ['39', '40', '41'])
    _map_csv_date(data, 'DDEPAM', dates.departure_last_place_of_landing if dates else None,
                  ['', 'B', 'C'])
    _map_csv_date(data, 'DATARR4', dates.voyage_completed if dates else None, '345')
    data['EVGREEN'] = voyage.voyage_in_cd_rom
    data['VOYAGE'] = dates.length_middle_passage_days if dates else None
    data['YEARDEP'] = VoyageDates.get_date_year(dates.imp_voyage_began if dates else None)
    data['YEARAF'] = VoyageDates.get_date_year(dates.imp_departed_africa if dates else None)
    yearam = VoyageDates.get_date_year(dates.imp_arrival_at_port_of_dis if dates else None)
    data['YEARAM'] = yearam
    data['VOY1IMP'] = dates.imp_length_home_to_disembark if dates else None
    data['VOY2IMP'] = dates.imp_length_leaving_africa_to_disembark if dates else None
    data['YEAR5'] = year_mod(yearam, 5, 1500)
    data['YEAR10'] = year_mod(yearam, 10, 1500)
    data['YEAR25'] = year_mod(yearam, 25, 1500)
    data['YEAR100'] = (year_mod(yearam, 100, 0) - 1) * 100 if yearam else None

    # Comments
    data['COMMENTS'] = voyage.comments

    # Outcomes
    outcomes = list(voyage.voyage_name_outcome.all())
    if len(outcomes) == 1:
        outcomes = outcomes[0]
        data['FATE'] = _get_label_value(outcomes.particular_outcome)
        data['FATE2'] = _get_label_value(outcomes.outcome_slaves)
        data['FATE3'] = _get_label_value(outcomes.vessel_captured_outcome)
        data['FATE4'] = _get_label_value(outcomes.outcome_owner)
        data['RESISTANCE'] = _get_label_value(outcomes.resistance)

    # Ship
    ship = voyage.voyage_ship
    data['SHIPNAME'] = ship.ship_name if ship else None
    data['NATIONAL'] = _get_label_value(ship.nationality_ship if ship else None)
    data['TONNAGE'] = ship.tonnage if ship else None
    data['TONTYPE'] = _get_label_value(ship.ton_type if ship else None)
    data['RIG'] = _get_label_value(ship.rig_of_vessel if ship else None)
    data['GUNS'] = ship.guns_mounted if ship else None
    data['YRCONS'] = ship.year_of_construction if ship else None
    data['PLACCONS'] = _get_label_value(ship.vessel_construction_place if ship else None)
    data['CONSTREG'] = _get_label_value(ship.vessel_construction_region if ship else None)
    data['YRREG'] = ship.registered_year if ship else None
    data['PLACREG'] = _get_label_value(ship.registered_place if ship else None)
    data['REGISREG'] = _get_label_value(ship.registered_region if ship else None)
    data['NATINIMP'] = _get_label_value(ship.imputed_nationality if ship else None)
    data['TONMOD'] = ship.tonnage_mod if ship else None

    aux = list(get_multi_valued_column_suffix(16, True))
    all_owners = _captain_owner_helper.get_owners(voyage)
    for i, owner in enumerate(all_owners):
        if i >= len(aux):
            break
        data['OWNER' + aux[i]] = owner

    aux = list(get_multi_valued_column_suffix(3, True))
    all_captains = _captain_owner_helper.get_captains(voyage)
    for i, captain in enumerate(all_captains):
        if i >= len(aux):
            break
        data['CAPTAIN' + aux[i]] = captain

    # Cargo
    aux = list(get_multi_valued_column_suffix(CARGO_COLUMN_COUNT, True))
    for i, cargo_conn in enumerate(voyage.cargo.all()):
        if i >= len(aux):
            break
        data['CARGOTYPE' + aux[i]] = cargo_conn.cargo_id
        data['CARGOUNIT' + aux[i]] = cargo_conn.unit_id
        data['CARGOAMOUNT' + aux[i]] = cargo_conn.amount

    # African info
    aux = list(get_multi_valued_column_suffix(3, True))
    for i, afrinfo in enumerate(voyage.african_info.all()):
        if i >= len(aux):
            break
        data['AFRINFO' + aux[i]] = afrinfo.id

    # Itinerary
    itinerary = voyage.voyage_itinerary
    data['PORTDEP'] = _get_label_value(itinerary.port_of_departure if itinerary else None)
    data['EMBPORT'] = _get_label_value(itinerary.int_first_port_emb if itinerary else None)
    data['EMBPORT2'] = _get_label_value(itinerary.int_second_port_emb if itinerary else None)
    data['EMBREG'] = _get_label_value(
        itinerary.int_first_region_purchase_slaves if itinerary else None)
    data['EMBREG2'] = _get_label_value(
        itinerary.int_second_region_purchase_slaves if itinerary else None)
    data['ARRPORT'] = _get_label_value(itinerary.int_first_port_dis if itinerary else None)
    data['ARRPORT2'] = _get_label_value(itinerary.int_second_port_dis if itinerary else None)
    data['ARRPORT3'] = _get_label_value(itinerary.int_third_port_dis if itinerary else None)
    data['ARRPORT4'] = _get_label_value(itinerary.int_fourth_port_dis if itinerary else None)
    data['REGARR'] = _get_label_value(itinerary.int_first_region_slave_landing if itinerary else None)
    data['REGARR2'] = _get_label_value(
        itinerary.int_second_place_region_slave_landing if itinerary else None)
    data['REGARR3'] = _get_label_value(
        itinerary.int_third_place_region_slave_landing if itinerary else None)
    data['REGARR4'] = _get_label_value(
        itinerary.int_fourth_place_region_slave_landing if itinerary else None)
    data['NPPRETRA'] = itinerary.ports_called_buying_slaves if itinerary else None
    data['PLAC1TRA'] = _get_label_value(itinerary.first_place_slave_purchase if itinerary else None)
    data['PLAC2TRA'] = _get_label_value(itinerary.second_place_slave_purchase if itinerary else None)
    data['PLAC3TRA'] = _get_label_value(itinerary.third_place_slave_purchase if itinerary else None)
    data['REGEM1'] = _get_label_value(itinerary.first_region_slave_emb if itinerary else None)
    data['REGEM2'] = _get_label_value(itinerary.second_region_slave_emb if itinerary else None)
    data['REGEM3'] = _get_label_value(itinerary.third_region_slave_emb if itinerary else None)
    data['NPAFTTRA'] = _get_label_value(
        itinerary.port_of_call_before_atl_crossing if itinerary else None)
    data['NPPRIOR'] = itinerary.number_of_ports_of_call if itinerary else None
    data['SLA1PORT'] = _get_label_value(itinerary.first_landing_place if itinerary else None)
    data['ADPSALE1'] = _get_label_value(itinerary.second_landing_place if itinerary else None)
    data['ADPSALE2'] = _get_label_value(itinerary.third_landing_place if itinerary else None)
    data['REGDIS1'] = _get_label_value(itinerary.first_landing_region if itinerary else None)
    data['REGDIS2'] = _get_label_value(itinerary.second_landing_region if itinerary else None)
    data['REGDIS3'] = _get_label_value(itinerary.third_landing_region if itinerary else None)
    data['PORTRET'] = _get_label_value(itinerary.place_voyage_ended if itinerary else None)
    data['RETRNREG'] = _get_label_value(itinerary.region_of_return if itinerary else None)
    data['RETRNREG1'] = _get_label_value(itinerary.broad_region_of_return if itinerary else None)
    data['MAJBUYPT'] = _get_label_value(
        itinerary.principal_place_of_slave_purchase if itinerary else None)
    data['MAJSELPT'] = _get_label_value(itinerary.principal_port_of_slave_dis if itinerary else None)
    data['PTDEPIMP'] = _get_label_value(itinerary.imp_port_voyage_begin if itinerary else None)
    data['MJBYPTIMP'] = _get_label_value(
        itinerary.imp_principal_place_of_slave_purchase if itinerary else None)
    data['MAJBYIMP'] = _get_label_value(
        itinerary.imp_principal_region_of_slave_purchase if itinerary else None)
    data['MAJBYIMP1'] = _get_label_value(
        itinerary.imp_broad_region_of_slave_purchase if itinerary else None)
    data['MJSLPTIMP'] = _get_label_value(
        itinerary.imp_principal_port_slave_dis if itinerary else None)
    data['MJSELIMP'] = _get_label_value(
        itinerary.imp_principal_region_slave_dis if itinerary else None)
    data['MJSELIMP1'] = _get_label_value(itinerary.imp_broad_region_slave_dis if itinerary else None)
    data['DEPTREGIMP'] = _get_label_value(itinerary.imp_region_voyage_begin if itinerary else None)
    data['DEPTREGIMP1'] = _get_label_value(
        itinerary.imp_broad_region_voyage_begin if itinerary else None)

    # Crew
    crew = voyage.voyage_crew
    data['CREW1'] = crew.crew_voyage_outset if crew else None
    data['CREW2'] = crew.crew_departure_last_port if crew else None
    data['CREW3'] = crew.crew_first_landing if crew else None
    data['CREW4'] = crew.crew_return_begin if crew else None
    data['CREW5'] = crew.crew_end_voyage if crew else None
    data['CREW'] = crew.unspecified_crew if crew else None
    data['SAILD1'] = crew.crew_died_before_first_trade if crew else None
    data['SAILD2'] = crew.crew_died_while_ship_african if crew else None
    data['SAILD3'] = crew.crew_died_middle_passage if crew else None
    data['SAILD4'] = crew.crew_died_in_americas if crew else None
    data['SAILD5'] = crew.crew_died_on_return_voyage if crew else None
    data['CREWDIED'] = crew.crew_died_complete_voyage if crew else None
    data['NDESERT'] = crew.crew_deserted if crew else None

    # Numbers
    numbers = voyage.voyage_slaves_numbers
    data['SLADAFRI'] = numbers.slave_deaths_before_africa if numbers else None
    data['SLADVOY'] = numbers.slave_deaths_between_africa_america if numbers else None
    data['SLADAMER'] = numbers.slave_deaths_between_arrival_and_sale if numbers else None
    data['SLINTEND'] = numbers.num_slaves_intended_first_port if numbers else None
    data['SLINTEN2'] = numbers.num_slaves_intended_second_port if numbers else None
    data['NCAR13'] = numbers.num_slaves_carried_first_port if numbers else None
    data['NCAR15'] = numbers.num_slaves_carried_second_port if numbers else None
    data['NCAR17'] = numbers.num_slaves_carried_third_port if numbers else None
    data['TSLAVESP'] = numbers.total_num_slaves_purchased if numbers else None
    data['TSLAVESD'] = numbers.total_num_slaves_dep_last_slaving_port if numbers else None
    data['SLAARRIV'] = numbers.total_num_slaves_arr_first_port_embark if numbers else None
    data['SLAS32'] = numbers.num_slaves_disembark_first_place if numbers else None
    data['SLAS36'] = numbers.num_slaves_disembark_second_place if numbers else None
    data['SLAS39'] = numbers.num_slaves_disembark_third_place if numbers else None
    data['SLAXIMP'] = numbers.imp_total_num_slaves_embarked if numbers else None
    data['SLAMIMP'] = numbers.imp_total_num_slaves_disembarked if numbers else None
    data['JAMCASPR'] = numbers.imp_jamaican_cash_price if numbers else None
    data['VYMRTIMP'] = numbers.imp_mortality_during_voyage if numbers else None
    data['MEN1'] = numbers.num_men_embark_first_port_purchase if numbers else None
    data['WOMEN1'] = numbers.num_women_embark_first_port_purchase if numbers else None
    data['BOY1'] = numbers.num_boy_embark_first_port_purchase if numbers else None
    data['GIRL1'] = numbers.num_girl_embark_first_port_purchase if numbers else None
    data['ADULT1'] = numbers.num_adult_embark_first_port_purchase if numbers else None
    data['CHILD1'] = numbers.num_child_embark_first_port_purchase if numbers else None
    data['INFANT1'] = numbers.num_infant_embark_first_port_purchase if numbers else None
    data['MALE1'] = numbers.num_males_embark_first_port_purchase if numbers else None
    data['FEMALE1'] = numbers.num_females_embark_first_port_purchase if numbers else None
    data['MEN2'] = numbers.num_men_died_middle_passage if numbers else None
    data['WOMEN2'] = numbers.num_women_died_middle_passage if numbers else None
    data['BOY2'] = numbers.num_boy_died_middle_passage if numbers else None
    data['GIRL2'] = numbers.num_girl_died_middle_passage if numbers else None
    data['ADULT2'] = numbers.num_adult_died_middle_passage if numbers else None
    data['CHILD2'] = numbers.num_child_died_middle_passage if numbers else None
    data['INFANT2'] = numbers.num_infant_died_middle_passage if numbers else None
    data['MALE2'] = numbers.num_males_died_middle_passage if numbers else None
    data['FEMALE2'] = numbers.num_females_died_middle_passage if numbers else None
    data['MEN3'] = numbers.num_men_disembark_first_landing if numbers else None
    data['WOMEN3'] = numbers.num_women_disembark_first_landing if numbers else None
    data['BOY3'] = numbers.num_boy_disembark_first_landing if numbers else None
    data['GIRL3'] = numbers.num_girl_disembark_first_landing if numbers else None
    data['ADULT3'] = numbers.num_adult_disembark_first_landing if numbers else None
    data['CHILD3'] = numbers.num_child_disembark_first_landing if numbers else None
    data['INFANT3'] = numbers.num_infant_disembark_first_landing if numbers else None
    data['MALE3'] = numbers.num_males_disembark_first_landing if numbers else None
    data['FEMALE3'] = numbers.num_females_disembark_first_landing if numbers else None
    data['MEN4'] = numbers.num_men_embark_second_port_purchase if numbers else None
    data['WOMEN4'] = numbers.num_women_embark_second_port_purchase if numbers else None
    data['BOY4'] = numbers.num_boy_embark_second_port_purchase if numbers else None
    data['GIRL4'] = numbers.num_girl_embark_second_port_purchase if numbers else None
    data['ADULT4'] = numbers.num_adult_embark_second_port_purchase if numbers else None
    data['CHILD4'] = numbers.num_child_embark_second_port_purchase if numbers else None
    data['INFANT4'] = numbers.num_infant_embark_second_port_purchase if numbers else None
    data['MALE4'] = numbers.num_males_embark_second_port_purchase if numbers else None
    data['FEMALE4'] = numbers.num_females_embark_second_port_purchase if numbers else None
    data['MEN5'] = numbers.num_men_embark_third_port_purchase if numbers else None
    data['WOMEN5'] = numbers.num_women_embark_third_port_purchase if numbers else None
    data['BOY5'] = numbers.num_boy_embark_third_port_purchase if numbers else None
    data['GIRL5'] = numbers.num_girl_embark_third_port_purchase if numbers else None
    data['ADULT5'] = numbers.num_adult_embark_third_port_purchase if numbers else None
    data['CHILD5'] = numbers.num_child_embark_third_port_purchase if numbers else None
    data['INFANT5'] = numbers.num_infant_embark_third_port_purchase if numbers else None
    data['MALE5'] = numbers.num_males_embark_third_port_purchase if numbers else None
    data['FEMALE5'] = numbers.num_females_embark_third_port_purchase if numbers else None
    data['MEN6'] = numbers.num_men_disembark_second_landing if numbers else None
    data['WOMEN6'] = numbers.num_women_disembark_second_landing if numbers else None
    data['BOY6'] = numbers.num_boy_disembark_second_landing if numbers else None
    data['GIRL6'] = numbers.num_girl_disembark_second_landing if numbers else None
    data['ADULT6'] = numbers.num_adult_disembark_second_landing if numbers else None
    data['CHILD6'] = numbers.num_child_disembark_second_landing if numbers else None
    data['INFANT6'] = numbers.num_infant_disembark_second_landing if numbers else None
    data['MALE6'] = numbers.num_males_disembark_second_landing if numbers else None
    data['FEMALE6'] = numbers.num_females_disembark_second_landing if numbers else None
    data['ADLT1IMP'] = numbers.imp_num_adult_embarked if numbers else None
    data['CHIL1IMP'] = numbers.imp_num_children_embarked if numbers else None
    data['MALE1IMP'] = numbers.imp_num_male_embarked if numbers else None
    data['FEML1IMP'] = numbers.imp_num_female_embarked if numbers else None
    data['SLAVEMA1'] = numbers.total_slaves_embarked_age_identified if numbers else None
    data['SLAVEMX1'] = numbers.total_slaves_embarked_gender_identified if numbers else None
    data['ADLT2IMP'] = numbers.imp_adult_death_middle_passage if numbers else None
    data['CHIL2IMP'] = numbers.imp_child_death_middle_passage if numbers else None
    data['MALE2IMP'] = numbers.imp_male_death_middle_passage if numbers else None
    data['FEML2IMP'] = numbers.imp_female_death_middle_passage if numbers else None
    data['ADLT3IMP'] = numbers.imp_num_adult_landed if numbers else None
    data['CHIL3IMP'] = numbers.imp_num_child_landed if numbers else None
    data['MALE3IMP'] = numbers.imp_num_male_landed if numbers else None
    data['FEML3IMP'] = numbers.imp_num_female_landed if numbers else None
    data['SLAVEMA3'] = numbers.total_slaves_landed_age_identified if numbers else None
    data['SLAVEMX3'] = numbers.total_slaves_landed_gender_identified if numbers else None
    data['SLAVEMA7'] = numbers.total_slaves_dept_or_arr_age_identified if numbers else None
    data['SLAVEMX7'] = numbers.total_slaves_dept_or_arr_gender_identified if numbers else None
    data['SLAVMAX1'] = numbers.total_slaves_embarked_age_gender_identified if numbers else None
    data['SLAVMAX3'] = (
        numbers.total_slaves_by_age_gender_identified_among_landed if numbers else None)
    data['SLAVMAX7'] = (
        numbers.total_slaves_by_age_gender_identified_departure_or_arrival if numbers else None)
    data['TSLMTIMP'] = numbers.imp_slaves_embarked_for_mortality if numbers else None
    data['MEN7'] = numbers.imp_num_men_total if numbers else None
    data['WOMEN7'] = numbers.imp_num_women_total if numbers else None
    data['BOY7'] = numbers.imp_num_boy_total if numbers else None
    data['GIRL7'] = numbers.imp_num_girl_total if numbers else None
    data['ADULT7'] = numbers.imp_num_adult_total if numbers else None
    data['CHILD7'] = numbers.imp_num_child_total if numbers else None
    data['MALE7'] = numbers.imp_num_males_total if numbers else None
    data['FEMALE7'] = numbers.imp_num_females_total if numbers else None
    data['MENRAT7'] = numbers.percentage_men if numbers else None
    data['WOMRAT7'] = numbers.percentage_women if numbers else None
    data['BOYRAT7'] = numbers.percentage_boy if numbers else None
    data['GIRLRAT7'] = numbers.percentage_girl if numbers else None
    data['MALRAT7'] = numbers.percentage_male if numbers else None
    data['CHILRAT7'] = numbers.percentage_child if numbers else None
    data['VYMRTRAT'] = numbers.imp_mortality_ratio if numbers else None
    data["BOYRAT1"] = numbers.percentage_boys_among_embarked_slaves if numbers else None
    data["CHILRAT1"] = numbers.child_ratio_among_embarked_slaves if numbers else None
    data["GIRLRAT1"] = numbers.percentage_girls_among_embarked_slaves if numbers else None
    data["MALRAT1"] = numbers.male_ratio_among_embarked_slaves if numbers else None
    data["MENRAT1"] = numbers.percentage_men_among_embarked_slaves if numbers else None
    data["WOMRAT1"] = numbers.percentage_women_among_embarked_slaves if numbers else None
    data["BOYRAT3"] = numbers.percentage_boys_among_landed_slaves if numbers else None
    data["CHILRAT3"] = numbers.child_ratio_among_landed_slaves if numbers else None
    data["GIRLRAT3"] = numbers.percentage_girls_among_landed_slaves if numbers else None
    data["MALRAT3"] = numbers.male_ratio_among_landed_slaves if numbers else None
    data["MENRAT3"] = numbers.percentage_men_among_landed_slaves if numbers else None
    data["WOMRAT3"] = numbers.percentage_women_among_landed_slaves if numbers else None
    # INSERT HERE any new number variables [export CSV]

    aux = list(get_multi_valued_column_suffix(18, True))
    for i, source_conn in enumerate(voyage.group.all()):
        if i >= len(aux):
            break
        data['SOURCE' + aux[i]] = source_conn.text_ref

    data['XMIMPFLAG'] = _get_label_value(voyage.voyage_groupings)

    # Links
    links = [
        str(link.second.voyage_id)
        for link in voyage.outgoing_to_other_voyages.all()
    ]
    data['VOYAGEID2'] = '/'.join(links)

    return data


def _map_interim_to_spss(interim):
    data = {}

    _map_csv_date(data, 'DATEDEP', interim.date_departure)
    _map_csv_date(data, 'D1SLATR', interim.date_slave_purchase_began)
    _map_csv_date(data, 'DLSLATR', interim.date_vessel_left_last_slaving_port)
    _map_csv_date(data, 'DATARR3', interim.date_first_slave_disembarkation,
                  '234')
    _map_csv_date(data, 'DATARR3', interim.date_second_slave_disembarkation,
                  '678')
    _map_csv_date(data, 'DATARR', interim.date_third_slave_disembarkation,
                  ['39', '40', '41'])
    _map_csv_date(data, 'DDEPAM',
                  interim.date_return_departure, ['', 'B', 'C'])
    _map_csv_date(data, 'DATARR4', interim.date_voyage_completed, '345')
    data['VOYAGE'] = interim.length_of_middle_passage

    # Ship, nation, owners
    data['SHIPNAME'] = interim.name_of_vessel
    data['NATIONAL'] = _get_label_value(interim.national_carrier)
    data['TONNAGE'] = interim.tonnage_of_vessel
    data['TONTYPE'] = _get_label_value(interim.ton_type)
    data['RIG'] = _get_label_value(interim.rig_of_vessel)
    data['GUNS'] = interim.guns_mounted
    data['YRCONS'] = interim.year_ship_constructed
    data['PLACCONS'] = _get_label_value(interim.ship_construction_place)
    data['CONSTREG'] = _get_region_value(interim.ship_construction_place)
    data['YRREG'] = interim.year_ship_registered
    data['PLACREG'] = _get_label_value(interim.ship_registration_place)
    data['REGISREG'] = _get_region_value(interim.ship_registration_place)
    data['OWNERA'] = interim.first_ship_owner
    data['OWNERB'] = interim.second_ship_owner
    other_ship_owners = _get_interim_additional_ship_owners(interim)
    aux = 'CDEFGHIJKLMNOP'
    for i, owner in enumerate(other_ship_owners):
        if i >= len(aux):
            break
        data['OWNER' + aux[i]] = owner

    data['CAPTAINA'] = interim.first_captain
    data['CAPTAINB'] = interim.second_captain
    data['CAPTAINC'] = interim.third_captain

    # Outcome
    data['FATE'] = _get_label_value(interim.voyage_outcome)
    data['RESISTANCE'] = _get_label_value(interim.african_resistance)

    # Itinerary
    data['PORTDEP'] = _get_label_value(interim.port_of_departure)
    data['EMBPORT'] = _get_label_value(interim.first_port_intended_embarkation)
    data['EMBPORT2'] = _get_label_value(
        interim.second_port_intended_embarkation)
    data['EMBREG'] = _get_region_value(interim.first_port_intended_embarkation)
    data['EMBREG2'] = _get_region_value(
        interim.second_port_intended_embarkation)
    data['ARRPORT'] = _get_label_value(
        interim.first_port_intended_disembarkation)
    data['ARRPORT2'] = _get_label_value(
        interim.second_port_intended_disembarkation)
    data['ARRPORT3'] = _get_label_value(
        interim.third_port_intended_disembarkation)
    data['ARRPORT4'] = _get_label_value(
        interim.fourth_port_intended_disembarkation)
    data['REGARR'] = _get_region_value(
        interim.first_port_intended_disembarkation)
    data['REGARR2'] = _get_region_value(
        interim.second_port_intended_disembarkation)
    data['REGARR3'] = _get_region_value(
        interim.third_port_intended_disembarkation)
    data['REGARR4'] = _get_region_value(
        interim.fourth_port_intended_disembarkation)
    data['NPPRETRA'] = interim.number_of_ports_called_prior_to_slave_purchase
    data['PLAC1TRA'] = _get_label_value(interim.first_place_of_slave_purchase)
    data['PLAC2TRA'] = _get_label_value(interim.second_place_of_slave_purchase)
    data['PLAC3TRA'] = _get_label_value(interim.third_place_of_slave_purchase)
    data['REGEM1'] = _get_region_value(interim.first_place_of_slave_purchase)
    data['REGEM2'] = _get_region_value(interim.second_place_of_slave_purchase)
    data['REGEM3'] = _get_region_value(interim.third_place_of_slave_purchase)
    data['NPAFTTRA'] = _get_label_value(
        interim.place_of_call_before_atlantic_crossing)
    data['NPPRIOR'] = (
        interim.number_of_new_world_ports_called_prior_to_disembarkation)
    data['SLA1PORT'] = _get_label_value(interim.first_place_of_landing)
    data['ADPSALE1'] = _get_label_value(interim.second_place_of_landing)
    data['ADPSALE2'] = _get_label_value(interim.third_place_of_landing)
    data['REGDIS1'] = _get_region_value(interim.first_place_of_landing)
    data['REGDIS2'] = _get_region_value(interim.second_place_of_landing)
    data['REGDIS3'] = _get_region_value(interim.third_place_of_landing)
    data['PORTRET'] = _get_label_value(interim.port_voyage_ended)
    data['RETRNREG'] = _get_region_value(interim.port_voyage_ended)
    data['RETRNREG1'] = (interim.port_voyage_ended.region.broad_region.value
                         if interim.port_voyage_ended else None)
    data['MAJBUYPT'] = _get_label_value(
        interim.principal_place_of_slave_purchase)
    data['MAJSELPT'] = _get_label_value(
        interim.principal_place_of_slave_disembarkation)

    # Imputed variables
    data['NATINIMP'] = _get_label_value(interim.imputed_national_carrier)
    data['TONMOD'] = interim.imputed_standardized_tonnage
    data['FATE2'] = _get_label_value(
        interim.imputed_outcome_of_voyage_for_slaves)
    data['FATE3'] = _get_label_value(
        interim.imputed_outcome_of_voyage_if_ship_captured)
    data['FATE4'] = _get_label_value(
        interim.imputed_outcome_of_voyage_for_owner)
    data['PTDEPIMP'] = _get_label_value(
        interim.imputed_port_where_voyage_began)
    data['MJBYPTIMP'] = _get_label_value(
        interim.imputed_principal_place_of_slave_purchase)
    data['MJSLPTIMP'] = _get_label_value(
        interim.imputed_principal_port_of_slave_disembarkation)
    data['DEPTREGIMP'] = _get_label_value(
        interim.imputed_region_where_voyage_began)
    # TODO: we should check why we have REGDIS1/REGEM vars being both imputed
    # and not imputed. Is this a design error?
    data['REGDIS1'] = _get_label_value(
        interim.imputed_first_region_of_slave_landing)
    data['REGDIS2'] = _get_label_value(
        interim.imputed_second_region_of_slave_landing)
    data['REGDIS3'] = _get_label_value(
        interim.imputed_third_region_of_slave_landing)
    data['REGEM1'] = _get_label_value(
        interim.imputed_first_region_of_embarkation_of_slaves)
    data['REGEM2'] = _get_label_value(
        interim.imputed_second_region_of_embarkation_of_slaves)
    data['REGEM3'] = _get_label_value(
        interim.imputed_third_region_of_embarkation_of_slaves)
    data['YEARDEP'] = interim.imputed_year_voyage_began
    data['YEARAF'] = interim.imputed_year_departed_africa
    data['YEARAM'] = interim.imputed_year_arrived_at_port_of_disembarkation
    data['YEAR5'] = interim.imputed_quinquennium_in_which_voyage_occurred
    data['YEAR10'] = interim.imputed_decade_in_which_voyage_occurred
    data['YEAR25'] = interim.imputed_quarter_century_in_which_voyage_occurred
    data['YEAR100'] = interim.imputed_century_in_which_voyage_occurred
    data['VOY1IMP'] = (
        interim.imputed_voyage_length_home_port_to_first_port_of_disembarkation)
    data['VOY2IMP'] = interim.imputed_length_of_middle_passage
    data['XMIMPFLAG'] = _get_label_value(
        interim.imputed_voyage_groupings_for_estimating_imputed_slaves)
    data['SLAXIMP'] = interim.imputed_total_slaves_embarked
    data['SLAMIMP'] = interim.imputed_total_slaves_disembarked
    data['TSLMTIMP'] = (
        interim.imputed_number_of_slaves_embarked_for_mortality_calculation)
    data['VYMRTIMP'] = (
        interim.imputed_total_slave_deaths_during_middle_passage)
    data['VYMRTRAT'] = interim.imputed_mortality_rate
    data['JAMCASPR'] = interim.imputed_standardized_price_of_slaves

    # Sources
    created_sources = list(chain(
        interim.article_sources.all(),
        interim.book_sources.all(),
        interim.newspaper_sources.all(),
        interim.private_note_or_collection_sources.all(),
        interim.unpublished_secondary_sources.all(),
        interim.primary_sources.all()))
    source_refs = [x.source_ref_text for x in created_sources] + \
        [x.full_ref for x in interim.pre_existing_sources.all()]
    aux = list(get_multi_valued_column_suffix(18, True))
    for i, ref in enumerate(source_refs):
        if i >= len(aux):
            break
        data['SOURCE' + aux[i]] = ref

    # Numerical variables
    for n in interim.slave_numbers.all():
        data[n.var_name] = n.number

    return data


def _save_editorial_version(review_request,
                            contrib_type,
                            in_cd_rom_override=None):
    editor_contribution = review_request.editor_contribution.first()
    if editor_contribution is None or \
            editor_contribution.interim_voyage is None:
        raise Exception(
            'This type of contribution requires an editor review interim '
            'voyage for publication'
        )
    interim = editor_contribution.interim_voyage
    # Create or load a voyage with the appropriate voyage id.
    voyage = Voyage()
    contrib = review_request.contribution()
    if contrib_type in ('merge', 'new'):
        if not review_request.created_voyage_id:
            raise Exception(
                'For new or merged contributions, an explicit voyage_id '
                'must be set'
            )
        voyage.voyage_id = review_request.created_voyage_id
    elif contrib_type == 'edit':
        voyage = Voyage.all_dataset_objects.get(
            voyage_id=contrib.edited_voyage_id)
    else:
        raise Exception('Unsupported contribution type ' + str(contrib_type))

    # Edit field values and create child records for the voyage.
    if contrib_type != 'edit':
        voyage.voyage_in_cd_rom = (in_cd_rom_override
                                   if in_cd_rom_override is not None
                                   else False)
    else:
        _delete_child_fk(voyage, 'voyage_ship')
        _delete_child_fk(voyage, 'voyage_itinerary')
        _delete_child_fk(voyage, 'voyage_dates')
        _delete_child_fk(voyage, 'voyage_crew')
        _delete_child_fk(voyage, 'voyage_slaves_numbers')
        voyage.voyage_name_outcome.clear()
        voyage.voyage_sources.clear()
        if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE <= 2:
            voyage.voyage_captain.clear()
            voyage.voyage_ship_owner.clear()

    voyage.dataset = review_request.dataset
    voyage.comments = interim.voyage_comments
    # Save voyage so that the database generates a primary key for it.
    voyage.voyage_groupings = (
        interim.imputed_voyage_groupings_for_estimating_imputed_slaves)
    voyage.save()

    def region(place):
        return None if place is None else place.region

    def broad_region(place):
        r = region(place)
        return None if r is None else r.broad_region

    # Voyage Ship
    ship = VoyageShip()
    ship.voyage = voyage
    ship.ship_name = interim.name_of_vessel
    ship.nationality_ship = interim.national_carrier
    ship.tonnage = interim.tonnage_of_vessel
    ship.ton_type = interim.ton_type
    ship.rig_of_vessel = interim.rig_of_vessel
    ship.guns_mounted = interim.guns_mounted
    ship.year_of_construction = interim.year_ship_constructed
    ship.vessel_construction_place = interim.ship_construction_place
    ship.vessel_construction_region = interim.imputed_region_ship_constructed
    ship.registered_year = interim.year_ship_registered
    ship.registered_place = interim.ship_registration_place
    ship.registered_region = region(interim.ship_registration_place)
    ship.imputed_nationality = interim.imputed_national_carrier
    ship.tonnage_mod = interim.imputed_standardized_tonnage
    ship.save()

    # Voyage Ship Owners
    def create_ship_owner(owner_name, order):
        if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE <= 2:
            owner = VoyageShipOwner()
            owner.name = owner_name
            owner.save()
            conn = VoyageShipOwnerConnection()
            conn.owner = owner
            conn.owner_order = order
            conn.voyage = voyage
            conn.save()
        if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE >= 2:
            # TODO detect existing alias/identity and create connection or
            # create new identity/alias if needed.
            pass

    if interim.first_ship_owner:
        create_ship_owner(interim.first_ship_owner, 1)
    if interim.second_ship_owner:
        create_ship_owner(interim.second_ship_owner, 2)
    additional_ship_owners = _get_interim_additional_ship_owners(interim)
    for index, owner in enumerate(additional_ship_owners):
        create_ship_owner(owner, index + 3)

    # Voyage Ship Captains
    def create_captain(name, order):
        if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE <= 2:
            captain = VoyageCaptain()
            captain.name = name
            captain.save()
            conn = VoyageCaptainConnection()
            conn.captain = captain
            conn.captain_order = order
            conn.voyage = voyage
            conn.save()
        if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE >= 2:
            # TODO detect existing alias/identity and create connection or
            # create new identity/alias if needed.
            pass

    if interim.first_captain:
        create_captain(interim.first_captain, 1)
    if interim.second_captain:
        create_captain(interim.second_captain, 2)
    if interim.third_captain:
        create_captain(interim.third_captain, 3)

    # Voyage Itinerary
    itinerary = VoyageItinerary()
    itinerary.voyage = voyage
    itinerary.port_of_departure = interim.port_of_departure
    itinerary.int_first_port_emb = interim.first_port_intended_embarkation
    itinerary.int_second_port_emb = interim.second_port_intended_embarkation
    itinerary.int_first_region_purchase_slaves = region(
        interim.first_port_intended_embarkation)
    itinerary.int_second_region_purchase_slaves = region(
        interim.second_port_intended_embarkation)
    itinerary.int_first_port_dis = (
        interim.first_port_intended_disembarkation)
    itinerary.int_second_port_dis = (
        interim.second_port_intended_disembarkation)
    itinerary.int_third_port_dis = interim.third_port_intended_disembarkation
    itinerary.int_fourth_port_dis = interim.fourth_port_intended_disembarkation
    itinerary.int_first_region_slave_landing = region(
        interim.first_port_intended_disembarkation)
    itinerary.int_second_place_region_slave_landing = region(
        interim.second_port_intended_disembarkation)
    itinerary.int_third_place_region_slave_landing = region(
        interim.third_port_intended_disembarkation)
    itinerary.int_fourth_place_region_slave_landing = region(
        interim.fourth_port_intended_disembarkation)
    itinerary.ports_called_buying_slaves = (
        interim.number_of_ports_called_prior_to_slave_purchase)
    itinerary.first_place_slave_purchase = (
        interim.first_place_of_slave_purchase)
    itinerary.second_place_slave_purchase = (
        interim.second_place_of_slave_purchase)
    itinerary.third_place_slave_purchase = (
        interim.third_place_of_slave_purchase)
    itinerary.first_region_slave_emb = region(
        interim.first_place_of_slave_purchase)
    itinerary.second_region_slave_emb = region(
        interim.second_place_of_slave_purchase)
    itinerary.third_region_slave_emb = region(
        interim.third_place_of_slave_purchase)
    itinerary.port_of_call_before_atl_crossing = (
        interim.place_of_call_before_atlantic_crossing)
    itinerary.number_of_ports_of_call = (
        interim.number_of_new_world_ports_called_prior_to_disembarkation)
    itinerary.first_landing_place = interim.first_place_of_landing
    itinerary.second_landing_place = interim.second_place_of_landing
    itinerary.third_landing_place = interim.third_place_of_landing
    itinerary.first_landing_region = region(interim.first_place_of_landing)
    itinerary.second_landing_region = region(interim.second_place_of_landing)
    itinerary.third_landing_region = region(interim.third_place_of_landing)
    itinerary.place_voyage_ended = interim.port_voyage_ended
    itinerary.region_of_return = region(interim.port_voyage_ended)
    itinerary.broad_region_of_return = broad_region(interim.port_voyage_ended)
    itinerary.imp_port_voyage_begin = interim.imputed_port_where_voyage_began
    itinerary.imp_region_voyage_begin = (
        interim.imputed_region_where_voyage_began)
    itinerary.imp_broad_region_voyage_begin = broad_region(
        interim.imputed_port_where_voyage_began)
    itinerary.principal_place_of_slave_purchase = (
        interim.principal_place_of_slave_purchase)
    itinerary.imp_principal_place_of_slave_purchase = (
        interim.imputed_principal_place_of_slave_purchase)
    itinerary.imp_principal_region_of_slave_purchase = region(
        interim.imputed_principal_place_of_slave_purchase)
    itinerary.imp_broad_region_of_slave_purchase = broad_region(
        interim.imputed_principal_place_of_slave_purchase)
    itinerary.principal_port_of_slave_dis = (
        interim.principal_place_of_slave_disembarkation)
    itinerary.imp_principal_port_slave_dis = (
        interim.imputed_principal_port_of_slave_disembarkation)
    itinerary.imp_principal_region_slave_dis = region(
        interim.imputed_principal_port_of_slave_disembarkation)
    itinerary.imp_broad_region_slave_dis = broad_region(
        interim.imputed_principal_port_of_slave_disembarkation)
    itinerary.save()

    # Voyage Outcome
    outcome = VoyageOutcome()
    outcome.voyage = voyage
    outcome.particular_outcome = interim.voyage_outcome
    outcome.resistance = interim.african_resistance
    outcome.outcome_slaves = interim.imputed_outcome_of_voyage_for_slaves
    outcome.vessel_captured_outcome = (
        interim.imputed_outcome_of_voyage_if_ship_captured)
    outcome.outcome_owner = interim.imputed_outcome_of_voyage_for_owner
    outcome.save()

    # Voyage dates.
    def year_dummies(year):
        try:
            year_int = int(year)
            return ',,' + str(year_int)
        except Exception:
            return ',,'

    dates = VoyageDates()
    dates.voyage = voyage
    dates.voyage_began = interim.date_departure
    dates.slave_purchase_began = interim.date_slave_purchase_began
    dates.vessel_left_port = interim.date_vessel_left_last_slaving_port
    dates.first_dis_of_slaves = interim.date_first_slave_disembarkation
    # dates.date_departed_africa = interim.???  TODO: check this
    dates.arrival_at_second_place_landing = (
        interim.date_second_slave_disembarkation)
    dates.third_dis_of_slaves = interim.date_third_slave_disembarkation
    dates.departure_last_place_of_landing = interim.date_return_departure
    dates.voyage_completed = interim.date_voyage_completed
    dates.length_middle_passage_days = interim.length_of_middle_passage
    dates.imp_voyage_began = year_dummies(interim.imputed_year_voyage_began)
    dates.imp_departed_africa = year_dummies(
        interim.imputed_year_departed_africa)
    dates.imp_arrival_at_port_of_dis = year_dummies(
        interim.imputed_year_arrived_at_port_of_disembarkation)
    dates.imp_length_home_to_disembark = (
        interim.imputed_voyage_length_home_port_to_first_port_of_disembarkation)
    dates.imp_length_leaving_africa_to_disembark = (
        interim.imputed_length_of_middle_passage)
    dates.save()

    numbers = {
        n.var_name.upper(): n.number for n in interim.slave_numbers.all()
    }

    # Voyage crew
    crew = VoyageCrew()
    crew.voyage = voyage
    crew.crew_voyage_outset = numbers.get('CREW1')
    crew.crew_departure_last_port = numbers.get('CREW2')
    crew.crew_first_landing = numbers.get('CREW3')
    crew.crew_return_begin = numbers.get('CREW4')
    crew.crew_end_voyage = numbers.get('CREW5')
    crew.unspecified_crew = numbers.get('CREW')
    crew.crew_died_before_first_trade = numbers.get('SAILD1')
    crew.crew_died_while_ship_african = numbers.get('SAILD2')
    crew.crew_died_middle_passage = numbers.get('SAILD3')
    crew.crew_died_in_americas = numbers.get('SAILD4')
    crew.crew_died_on_return_voyage = numbers.get('SAILD5')
    crew.crew_died_complete_voyage = numbers.get('CREWDIED')
    crew.crew_deserted = numbers.get('NDESERT')
    crew.save()

    # Voyage slave numbers
    slaves_numbers = VoyageSlavesNumbers()
    slaves_numbers.voyage = voyage
    slaves_numbers.slave_deaths_before_africa = numbers.get('SLADAFRI')
    slaves_numbers.slave_deaths_between_africa_america = numbers.get('SLADVOY')
    slaves_numbers.slave_deaths_between_arrival_and_sale = numbers.get(
        'SLADAMER')
    slaves_numbers.num_slaves_intended_first_port = numbers.get('SLINTEND')
    slaves_numbers.num_slaves_intended_second_port = numbers.get('SLINTEN2')
    slaves_numbers.num_slaves_carried_first_port = numbers.get('NCAR13')
    slaves_numbers.num_slaves_carried_second_port = numbers.get('NCAR15')
    slaves_numbers.num_slaves_carried_third_port = numbers.get('NCAR17')
    slaves_numbers.total_num_slaves_purchased = numbers.get('TSLAVESP')
    slaves_numbers.total_num_slaves_dep_last_slaving_port = numbers.get(
        'TSLAVESD')
    slaves_numbers.total_num_slaves_arr_first_port_embark = numbers.get(
        'SLAARRIV')
    slaves_numbers.num_slaves_disembark_first_place = numbers.get('SLAS32')
    slaves_numbers.num_slaves_disembark_second_place = numbers.get('SLAS36')
    slaves_numbers.num_slaves_disembark_third_place = numbers.get('SLAS39')
    slaves_numbers.imp_total_num_slaves_embarked = (
        interim.imputed_total_slaves_embarked)
    slaves_numbers.imp_total_num_slaves_disembarked = (
        interim.imputed_total_slaves_disembarked)
    slaves_numbers.imp_jamaican_cash_price = (
        interim.imputed_standardized_price_of_slaves)
    slaves_numbers.imp_mortality_during_voyage = (
        interim.imputed_total_slave_deaths_during_middle_passage)
    slaves_numbers.num_men_embark_first_port_purchase = numbers.get('MEN1')
    slaves_numbers.num_women_embark_first_port_purchase = numbers.get('WOMEN1')
    slaves_numbers.num_boy_embark_first_port_purchase = numbers.get('BOY1')
    slaves_numbers.num_girl_embark_first_port_purchase = numbers.get('GIRL1')
    slaves_numbers.num_adult_embark_first_port_purchase = numbers.get('ADULT1')
    slaves_numbers.num_child_embark_first_port_purchase = numbers.get('CHILD1')
    slaves_numbers.num_infant_embark_first_port_purchase = numbers.get(
        'INFANT1')
    slaves_numbers.num_males_embark_first_port_purchase = numbers.get('MALE1')
    slaves_numbers.num_females_embark_first_port_purchase = numbers.get(
        'FEMALE1')
    slaves_numbers.num_men_died_middle_passage = numbers.get('MEN2')
    slaves_numbers.num_women_died_middle_passage = numbers.get('WOMEN2')
    slaves_numbers.num_boy_died_middle_passage = numbers.get('BOY2')
    slaves_numbers.num_girl_died_middle_passage = numbers.get('GIRL2')
    slaves_numbers.num_adult_died_middle_passage = numbers.get('ADULT2')
    slaves_numbers.num_child_died_middle_passage = numbers.get('CHILD2')
    slaves_numbers.num_infant_died_middle_passage = numbers.get('INFANT2')
    slaves_numbers.num_males_died_middle_passage = numbers.get('MALE2')
    slaves_numbers.num_females_died_middle_passage = numbers.get('FEMALE2')
    slaves_numbers.num_men_disembark_first_landing = numbers.get('MEN3')
    slaves_numbers.num_women_disembark_first_landing = numbers.get('WOMEN3')
    slaves_numbers.num_boy_disembark_first_landing = numbers.get('BOY3')
    slaves_numbers.num_girl_disembark_first_landing = numbers.get('GIRL3')
    slaves_numbers.num_adult_disembark_first_landing = numbers.get('ADULT3')
    slaves_numbers.num_child_disembark_first_landing = numbers.get('CHILD3')
    slaves_numbers.num_infant_disembark_first_landing = numbers.get('INFANT3')
    slaves_numbers.num_males_disembark_first_landing = numbers.get('MALE3')
    slaves_numbers.num_females_disembark_first_landing = numbers.get('FEMALE3')
    slaves_numbers.num_men_embark_second_port_purchase = numbers.get('MEN4')
    slaves_numbers.num_women_embark_second_port_purchase = numbers.get(
        'WOMEN4')
    slaves_numbers.num_boy_embark_second_port_purchase = numbers.get('BOY4')
    slaves_numbers.num_girl_embark_second_port_purchase = numbers.get('GIRL4')
    slaves_numbers.num_adult_embark_second_port_purchase = numbers.get(
        'ADULT4')
    slaves_numbers.num_child_embark_second_port_purchase = numbers.get(
        'CHILD4')
    slaves_numbers.num_infant_embark_second_port_purchase = numbers.get(
        'INFANT4')
    slaves_numbers.num_males_embark_second_port_purchase = numbers.get('MALE4')
    slaves_numbers.num_females_embark_second_port_purchase = numbers.get(
        'FEMALE4')
    slaves_numbers.num_men_embark_third_port_purchase = numbers.get('MEN5')
    slaves_numbers.num_women_embark_third_port_purchase = numbers.get('WOMEN5')
    slaves_numbers.num_boy_embark_third_port_purchase = numbers.get('BOY5')
    slaves_numbers.num_girl_embark_third_port_purchase = numbers.get('GIRL5')
    slaves_numbers.num_adult_embark_third_port_purchase = numbers.get('ADULT5')
    slaves_numbers.num_child_embark_third_port_purchase = numbers.get('CHILD5')
    slaves_numbers.num_infant_embark_third_port_purchase = numbers.get(
        'INFANT5')
    slaves_numbers.num_males_embark_third_port_purchase = numbers.get('MALE5')
    slaves_numbers.num_females_embark_third_port_purchase = numbers.get(
        'FEMALE5')
    slaves_numbers.num_men_disembark_second_landing = numbers.get('MEN6')
    slaves_numbers.num_women_disembark_second_landing = numbers.get('WOMEN6')
    slaves_numbers.num_boy_disembark_second_landing = numbers.get('BOY6')
    slaves_numbers.num_girl_disembark_second_landing = numbers.get('GIRL6')
    slaves_numbers.num_adult_disembark_second_landing = numbers.get('ADULT6')
    slaves_numbers.num_child_disembark_second_landing = numbers.get('CHILD6')
    slaves_numbers.num_infant_disembark_second_landing = numbers.get('INFANT6')
    slaves_numbers.num_males_disembark_second_landing = numbers.get('MALE6')
    slaves_numbers.num_females_disembark_second_landing = numbers.get(
        'FEMALE6')
    slaves_numbers.imp_num_adult_embarked = numbers.get('ADLT1IMP')
    slaves_numbers.imp_num_children_embarked = numbers.get('CHIL1IMP')
    slaves_numbers.imp_num_male_embarked = numbers.get('MALE1IMP')
    slaves_numbers.imp_num_female_embarked = numbers.get('FEML1IMP')
    slaves_numbers.total_slaves_embarked_age_identified = numbers.get(
        'SLAVEMA1')
    slaves_numbers.total_slaves_embarked_gender_identified = numbers.get(
        'SLAVEMX1')
    slaves_numbers.imp_adult_death_middle_passage = numbers.get('ADLT2IMP')
    slaves_numbers.imp_child_death_middle_passage = numbers.get('CHIL2IMP')
    slaves_numbers.imp_male_death_middle_passage = numbers.get('MALE2IMP')
    slaves_numbers.imp_female_death_middle_passage = numbers.get('FEML2IMP')
    slaves_numbers.imp_num_adult_landed = numbers.get('ADLT3IMP')
    slaves_numbers.imp_num_child_landed = numbers.get('CHIL3IMP')
    slaves_numbers.imp_num_male_landed = numbers.get('MALE3IMP')
    slaves_numbers.imp_num_female_landed = numbers.get('FEML3IMP')
    slaves_numbers.total_slaves_landed_age_identified = numbers.get('SLAVEMA3')
    slaves_numbers.total_slaves_landed_gender_identified = numbers.get(
        'SLAVEMX3')
    slaves_numbers.total_slaves_dept_or_arr_age_identified = numbers.get(
        'SLAVEMA7')
    slaves_numbers.total_slaves_dept_or_arr_gender_identified = numbers.get(
        'SLAVEMX7')
    slaves_numbers.imp_slaves_embarked_for_mortality = (
        interim.imputed_number_of_slaves_embarked_for_mortality_calculation)
    slaves_numbers.imp_num_men_total = numbers.get('MEN7')
    slaves_numbers.imp_num_women_total = numbers.get('WOMEN7')
    slaves_numbers.imp_num_boy_total = numbers.get('BOY7')
    slaves_numbers.imp_num_girl_total = numbers.get('GIRL7')
    slaves_numbers.imp_num_adult_total = numbers.get('ADULT7')
    slaves_numbers.imp_num_child_total = numbers.get('CHILD7')
    slaves_numbers.imp_num_males_total = numbers.get('MALE7')
    slaves_numbers.imp_num_females_total = numbers.get('FEMALE7')
    slaves_numbers.percentage_men = numbers.get('MENRAT7')
    slaves_numbers.percentage_women = numbers.get('WOMRAT7')
    slaves_numbers.percentage_boy = numbers.get('BOYRAT7')
    slaves_numbers.percentage_girl = numbers.get('GIRLRAT7')
    slaves_numbers.percentage_male = numbers.get('MALRAT7')
    slaves_numbers.percentage_child = numbers.get('CHILRAT7')
    slaves_numbers.percentage_adult = (
        1.0 - slaves_numbers.percentage_child
        if slaves_numbers.percentage_child is not None
        else None)
    slaves_numbers.percentage_female = (
        1.0 - slaves_numbers.percentage_male
        if slaves_numbers.percentage_male is not None
        else None)
    slaves_numbers.imp_mortality_ratio = interim.imputed_mortality_rate
    slaves_numbers.total_slaves_embarked_age_gender_identified = numbers.get(
        u'SLAVMAX1')
    slaves_numbers.total_slaves_by_age_gender_identified_among_landed = (
        numbers.get(u'SLAVMAX3'))
    slaves_numbers.total_slaves_by_age_gender_identified_departure_or_arrival = numbers.get(
        u'SLAVMAX7')
    slaves_numbers.percentage_boys_among_embarked_slaves = numbers.get(
        u'BOYRAT1')
    slaves_numbers.child_ratio_among_embarked_slaves = numbers.get(u'CHILRAT1')
    slaves_numbers.percentage_girls_among_embarked_slaves = numbers.get(
        u'GIRLRAT1')
    slaves_numbers.male_ratio_among_embarked_slaves = numbers.get(u'MALRAT1')
    slaves_numbers.percentage_men_among_embarked_slaves = numbers.get(
        u'MENRAT1')
    slaves_numbers.percentage_women_among_embarked_slaves = numbers.get(
        u'WOMRAT1')
    slaves_numbers.percentage_boys_among_landed_slaves = numbers.get(
        u'BOYRAT3')
    slaves_numbers.child_ratio_among_landed_slaves = numbers.get(u'CHILRAT3')
    slaves_numbers.percentage_girls_among_landed_slaves = numbers.get(
        u'GIRLRAT3')
    slaves_numbers.male_ratio_among_landed_slaves = numbers.get(u'MALRAT3')
    slaves_numbers.percentage_men_among_landed_slaves = numbers.get(u'MENRAT3')
    slaves_numbers.percentage_women_among_landed_slaves = numbers.get(
        u'WOMRAT3')
    # INSERT HERE any new number variables [publish from interim]
    slaves_numbers.save()

    # Voyage sources
    def create_source_connection(src, conn_ref, order):
        conn = VoyageSourcesConnection()
        conn.source = src
        conn.group = voyage
        conn.source_order = order
        conn.text_ref = conn_ref
        conn.save()

    def create_source_reference(short_ref, conn_ref, order):
        src = VoyageSources.objects.filter(short_ref=short_ref).first()
        if src is None:
            raise Exception('Source "' + short_ref + '" not found')
        create_source_connection(src, conn_ref, order)

    created_sources = list(chain(
        interim.article_sources.all(),
        interim.book_sources.all(),
        interim.newspaper_sources.all(),
        interim.private_note_or_collection_sources.all(),
        interim.unpublished_secondary_sources.all(),
        interim.primary_sources.all()))
    pre_existing_sources = list(interim.pre_existing_sources.all())
    if contrib_type != 'edit' and contrib_type != 'merge' and len(
            pre_existing_sources) > 0:
        raise Exception('A contribution with type '
                        '"' + contrib_type + '" '
                        'cannot have pre existing sources')
    source_order = 1
    for src in created_sources:
        # Each src here has as type a subclass of InterimContributedSource
        if not src.created_voyage_sources:
            raise Exception(
                'Invalid state: a new source must have been created to match '
                '"' + str(src.source_ref_text) + '"')
        create_source_connection(src.created_voyage_sources,
                                 src.source_ref_text, source_order)
        source_order += 1
    for src in pre_existing_sources:
        if src.action == InterimPreExistingSourceActions.exclude:
            continue
        create_source_reference(src.original_short_ref, src.original_ref,
                                source_order)
        source_order += 1

    Voyage.african_info.through.objects.filter(voyage=voyage).delete()
    if interim.african_info:
        afrinfo = json.loads(interim.african_info)
        for a in afrinfo:
            afrinfo_conn = Voyage.african_info.through(voyage_id=voyage.voyage_id, africaninfo_id=a)
            afrinfo_conn.save()
    VoyageCargoConnection.objects.filter(voyage=voyage).delete()
    if interim.cargo:
        cargo = json.loads(interim.cargo)
        for c in cargo:
            cargo_conn = VoyageCargoConnection()
            cargo_conn.voyage = voyage
            cargo_conn.cargo_id = c['cargo_type']
            cargo_conn.unit_id = c.get('unit')
            cargo_conn.amount = c.get('amount')
            cargo_conn.save()

    # Set voyage foreign keys (this is redundant, but we are keeping the
    # original model design)
    voyage.voyage_ship = ship
    voyage.voyage_itinerary = itinerary
    voyage.voyage_dates = dates
    voyage.voyage_crew = crew
    voyage.voyage_slaves_numbers = slaves_numbers
    voyage.save()

    return voyage


def _delete_voyages(ids):
    delete_voyages = list(Voyage.all_dataset_objects.filter(voyage_id__in=ids))
    if len(ids) != len(delete_voyages):
        raise Exception(
            "Voyage not found for deletion, voyage ids=" + str(ids))
    for v in delete_voyages:
        v.delete()


def _publish_single_review_delete(review_request, all_deleted_ids):
    contribution = review_request.contribution()
    ids = list(contribution.get_related_voyage_ids())
    _delete_voyages(ids)
    all_deleted_ids.extend(ids)


def _publish_single_review_merge(review_request, all_deleted_ids):
    contribution = review_request.contribution()
    # Delete previous records and create a new one to replace them.
    ids = list(contribution.get_related_voyage_ids())
    in_cd_rom_list = list(
        Voyage.all_dataset_objects.filter(voyage_id__in=ids).values_list(
            'voyage_in_cd_rom', flat=True))
    _delete_voyages(ids)
    all_deleted_ids.extend(ids)
    _save_editorial_version(review_request, 'merge', True in in_cd_rom_list)


def _publish_single_review_new(review_request):
    _save_editorial_version(review_request, 'new')


def _publish_single_review_update(review_request):
    _save_editorial_version(review_request, 'edit')
