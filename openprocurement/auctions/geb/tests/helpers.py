import iso8601
from collections import Mapping, Sequence
from openprocurement.auctions.geb.tests.specifications import STATUS_CHANGES
from openprocurement.auctions.geb.tests.fixtures import (
    test_question_data,
    test_bid_data
)


def get_error_description(error):
    if isinstance(error, Sequence):
        return error[0]
    elif isinstance(error, Mapping):
        return get_error_description(error.values()[0])

    return error


def get_errors_names(response):
    context = []
    errors = response.json.get('errors')

    if not errors:
        return None
    for error in errors:
        context.append(error['name'])

    return context


def get_specification_fields(scheme, field_type=None):
    context = []
    for field in scheme:
        field_name = field['name']

        if not field.get(field_type):
            continue
        if field.get('model'):
            required = {field_name: get_specification_fields(field['model'],
                                                             field_type=field_type)}
        else:
            required = field_name
        context.append(required)

    return context


def get_expected_value(scheme, check, order=0):

    def get_field():
        value = check[order] if isinstance(check, tuple) else check

        for field in scheme:
            if field.get('name') == value:
                return field
        return None

    field = get_field()
    if field.get('model'):
        return get_expected_value(field['model'], check, order=order + 1)
    else:
        return field.get('value')


def check_affilation(main, expected):
    for item in expected:
        if isinstance(item, Mapping):
            check_affilation(main.get(item.keys()[0]), item.values()[0])
        else:
            if not main.get(item):
                return item


def get_next_status(current):
    status = STATUS_CHANGES.get(current)
    if status:
        next_status = status.get('next_status')
        if next_status:
            return next_status[0]


def get_procedure_state(procedure, status):
    for state in procedure:
        if state.status == status:
            break
    return state


def get_period_duration(auction, period):
    start_date = auction[period]['startDate']
    end_date = auction[period]['endDate']
    return iso8601.parse_date(end_date) - iso8601.parse_date(start_date)


def create_question(test_case, auction):
    request_data = test_question_data
    entrypoint = '/auctions/{}/questions'.format(auction['id'])
    response = test_case.app.post_json(entrypoint, request_data)
    return response.json['data']


def create_active_bid(test_case, auction):
    auth = test_case.app.authorization

    bid_owner = ('Basic', ('broker', ''))
    test_case.app.authorization = bid_owner
    request_data = test_bid_data
    entrypoint = '/auctions/{}/bids'.format(auction['id'])
    response = test_case.app.post_json(entrypoint, request_data)

    bid = response.json['data']
    access = response.json['access']
    entrypoint = '/auctions/{}/bids/{}?acc_token={}'.format(auction['id'],
                                                            bid['id'],
                                                            access['token'])
    request_data = {"data": {"status": "pending"}}
    response = test_case.app.patch_json(entrypoint, request_data)

    test_case.app.authorization = auth
    return {'data': response.json['data'], 'access': access, 'owner': bid_owner}


def create_bid(test_case, auction):

    request_data = test_bid_data
    entrypoint = '/auctions/{}/bids'.format(auction['id'])
    response = test_case.app.post_json(entrypoint, request_data)

    bid = response.json['data']
    access = response.json['access']
    bid_owner = test_case.app.authorization

    return {'data': bid, 'access': access, 'owner': bid_owner}


def delete_bid(test_case, auction, bid, access):

    entrypoint = '/auctions/{}/bids/{}?acc_token={}'.format(auction['id'],
                                                            bid['id'],
                                                            access['token'])
    test_case.app.delete_json(entrypoint)


def set_auction_period(test_case, auction):

    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('chronograph', ''))
    request_data = {'data': {'id': auction['id']}}
    entrypoint = '/auctions/{}'.format(auction['id'])
    test_case.app.patch_json(entrypoint, request_data)

    test_case.app.authorization = auth
