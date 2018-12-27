from copy import deepcopy

from openprocurement.auctions.core.tests.base import (
    test_document_data
)

from openprocurement.auctions.geb.tests.fixtures.common import (
    # test_item,
    test_procuringEntity,
    test_lotHolder,
    test_bankAccount,
    test_contractTerms,
    test_question_data
)
from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.items import (
    TEST_ITEM
)


def change_title(test_case):
    new_title = 'New Title'
    field = "title"

    request_data = {"data": {field: new_title}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)

    test_case.assertEqual(new_title, response.json['data'][field])


def change_minNumberOfQualifiedBids(test_case):
    new = 1
    field = "minNumberOfQualifiedBids"

    request_data = {"data": {field: new}}
    test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertNotEqual(new, response.json['data'][field])


def change_one_field_rest_same(test_case):
    new_title = 'Test'
    field = "title"

    all_data = deepcopy(AUCTION)
    request_data = {"data": all_data}
    request_data['data'][field] = new_title
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)

    test_case.assertEqual(new_title, response.json['data'][field])


def change_title_dump(test_case):
    new_title = 'Test'
    field = "title"

    request_data = {"data": {field: new_title}}
    response = test_case.app.patch_json(test_case.ENTRYPOINT, request_data)

    filename = 'docs/source/tutorial/active_rectification_change_title.http'
    test_case.dump(response.request, response, filename)


def change_desctiption(test_case):
    new = 'Test'
    field = "description"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_tenderAttempts(test_case):
    field = "tenderAttempts"
    new = 2

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_lotIdentifier(test_case):
    new = '123456'
    field = "lotIdentifier"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_value(test_case):
    new = {u'currency': u'UAH', u'amount': 82.0, u'valueAddedTaxIncluded': True}
    field = "value"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_minimalStep(test_case):
    new = {u'currency': u'UAH', u'amount': 90.0, u'valueAddedTaxIncluded': True}
    field = "minimalStep"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_guarantee(test_case):
    new = {u'currency': u'UAH', u'amount': 42.0}
    field = "guarantee"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def item_get(test_case):
    expected_http_status = '200 OK'
    expected_data = [
        'description',
        'classification',
        'additionalClassifications',
        'address',
        'id',
        'unit',
        'quantity'
    ]
    response = test_case.app.get(test_case.ENTRYPOINTS['get_item'])
    item = response.json['data']

    test_case.assertEqual(response.status, expected_http_status)
    test_case.assertEqual(item.keys(), expected_data)


def item_patch(test_case):
    field = "quantity"
    new_value = 42

    request_data = {'data': {field: new_value}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_item'], request_data)
    item = response.json['data']

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(item[field], new_value)

    response = test_case.app.get(test_case.ENTRYPOINTS['get_item'])
    item = response.json['data']
    test_case.assertEqual(item[field], new_value)


def items_get_listing(test_case):
    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])
    auction = response.json['data']
    auction_items = [item['id'] for item in auction['items']]

    response = test_case.app.get(test_case.ENTRYPOINTS['get_items_collection'])
    items = response.json['data']
    for item in items:
        test_case.assertIn(item['id'], auction_items)


def items_patch_collections(test_case):
    items_data = [deepcopy(item['data']) for item in test_case.items]
    order = 0
    field = "quantity"
    new_value = 42

    items_data[order][field] = new_value
    request_data = {"data": {'items': items_data}}

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)

    auction = response.json['data']
    test_case.assertEqual(auction['items'][order][field], new_value)

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    auction = response.json['data']
    test_case.assertEqual(auction['items'][order][field], new_value)


def items_patch_collections_blank_items(test_case):

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])
    auction = response.json['data']
    items_before = auction['items']

    request_data = {"data": {'items': None}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    request_data = {"data": {'items': []}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data, status=403)
    test_case.assertEqual(response.status, '403 Forbidden')

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'])
    auction = response.json['data']
    items_after = auction['items']

    test_case.assertEqual(len(items_before), len(items_after))


def item_post(test_case):
    expected_http_status = '201 Created'

    request_data = {'data': TEST_ITEM}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['item_post'], request_data)
    test_case.assertEqual(response.status, expected_http_status)
    item = response.json['data']

    entrypoint = '/auctions/{}/items/{}'.format(test_case.auction['data']['id'], item['id'])
    response = test_case.app.get(entrypoint, request_data)
    test_case.assertEqual(response.status, '200 OK')


def change_budgetSpent(test_case):
    new = {u'currency': u'UAH', u'amount': 42.0, u'valueAddedTaxIncluded': True}
    field = "budgetSpent"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_registrationFee(test_case):
    new = {u'currency': u'UAH', u'amount': 800.0}
    field = "registrationFee"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_procuringEntity(test_case):
    procuringEntity = deepcopy(test_procuringEntity)
    procuringEntity['name'] = 'Test'
    new = procuringEntity
    field = "procuringEntity"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_lotHolder(test_case):
    lotHolder = deepcopy(test_lotHolder)
    lotHolder['name'] = 'Test'
    new = lotHolder
    field = "lotHolder"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_bankAccount(test_case):
    bankAccount = deepcopy(test_bankAccount)
    bankAccount['bankName'] = u'Test'
    new = bankAccount
    field = "bankAccount"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    response = test_case.app.get(test_case.ENTRYPOINTS['get_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])


def change_contractTerms(test_case):
    contractTerms = deepcopy(test_contractTerms)
    contractTerms['leaseTerms']['leaseDuration'] = u'P20Y'
    new = contractTerms
    field = "contractTerms"

    request_data = {"data": {field: new}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_auction'], request_data)
    test_case.assertEqual(new, response.json['data'][field])

    auction_entrypoint = '/auctions/{}'.format(test_case.auction['data']['id'])
    response = test_case.app.get(auction_entrypoint, request_data)
    test_case.assertEqual(new, response.json['data'][field])


# document tests


def auction_document_post_offline(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    document.pop('hash')
    document['accessDetails'] = 'test accessDetails'
    document['documentType'] = 'x_dgfAssetFamiliarization'

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['documents'], request_data)
    test_case.assertEqual(expected_http_status, response.status)


def auction_document_post(test_case):

    auction_documents_type = [
        'technicalSpecifications',
        'evaluationCriteria',
        'clarifications',
        'billOfQuantity',
        'conflictOfInterest',
        'evaluationReports',
        'complaints',
        'eligibilityCriteria',
        'tenderNotice',
        'illustration',
        'x_financialLicense',
        'x_virtualDataRoom',
        'x_presentation',
        'x_nda',
        'x_qualificationDocuments',
        'cancellationDetails',
        'contractProforma'
    ]
    init_document = deepcopy(test_document_data)
    init_document['url'] = test_case.generate_docservice_url()

    expected_http_status = '201 Created'
    for doc_type in auction_documents_type:
        document = deepcopy(init_document)
        document['documentType'] = doc_type

        request_data = {'data': document}
        response = test_case.app.post_json(test_case.ENTRYPOINTS['documents'], request_data)
        test_case.assertEqual(expected_http_status, response.status)


def auction_document_post_without_ds(test_case):

    file_title = 'name.doc'
    file_info = ('file', file_title, 'content')
    response = test_case.app.post(test_case.ENTRYPOINTS['documents'], upload_files=[file_info])

    test_case.assertEqual(response.status, '201 Created')
    test_case.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    test_case.assertIn(doc_id, response.headers['Location'])
    test_case.assertEqual(file_title, response.json["data"]["title"])


def auction_document_put_without_ds(test_case):
    file_title = 'name.doc'
    file_info = ('file', file_title, 'content')
    response = test_case.app.put(test_case.ENTRYPOINTS['document_put'], upload_files=[file_info])

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(response.content_type, 'application/json')
    test_case.assertEqual(file_title, response.json["data"]["title"])


def auction_document_patch(test_case):
    field = 'documentType'
    new = 'technicalSpecifications'

    request_data = {'data': {field: new}}

    response = test_case.app.patch_json(test_case.ENTRYPOINTS['document_patch'], request_data)
    document = response.json['data']

    test_case.assertEqual(response.status, '200 OK')
    test_case.assertEqual(document[field], new)

    response = test_case.app.get(test_case.ENTRYPOINTS['document_get'])
    document = response.json['data']
    test_case.assertEqual(document[field], new)


def auction_document_download(test_case):
    # get document data
    response = test_case.app.get(test_case.ENTRYPOINTS['document_get'])
    document_data = response.json['data']

    # get document key
    key = document_data["url"].split('?')[-1]

    # download document
    entrypoint_pattern = '/auctions/{}/documents/{}?download={}'
    entrypoint = entrypoint_pattern.format(test_case.auction['data']['id'],
                                           test_case.document['data']['id'],
                                           key)
    response = test_case.app.get(entrypoint)

    test_case.assertEqual(response.content_type, 'application/msword')


def auction_document_put(test_case):
    new_document = deepcopy(test_document_data)
    new_title = 'Title for new Document'
    url = test_case.generate_docservice_url(),
    new_document['url'] = url[0]
    new_document['title'] = new_title

    request_data = {'data': new_document}

    response = test_case.app.put_json(test_case.ENTRYPOINTS['document_put'], request_data)

    test_case.assertEqual(response.status, '200 OK')

    response = test_case.app.get(test_case.ENTRYPOINTS['document_get'])
    document = response.json['data']
    test_case.assertEqual(document['title'], new_title)


def add_document_dump(test_case):
    document = deepcopy(test_document_data)
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINT, request_data)

    filename = 'docs/source/tutorial/active_rectification_add_document.http'
    test_case.dump(response.request, response, filename)


def add_question(test_case):
    expected_http_status = '201 Created'

    request_data = test_question_data
    response = test_case.app.post_json(test_case.ENTRYPOINTS['post_question'], request_data)
    test_case.assertEqual(response.status, expected_http_status)

    question = response.json['data']

    auction_entrypoint = '/auctions/{}'.format(test_case.auction['data']['id'])

    response = test_case.app.get(auction_entrypoint)

    auction = response.json['data']
    questions = [question['id'] for question in auction['questions']]
    test_case.assertIn(question['id'], questions)

    question_url_pattern = '/auctions/{auction}/questions/{question}'
    question_url = question_url_pattern.format(auction=test_case.auction['data']['id'],
                                               question=question['id'])

    response = test_case.app.get(question_url)
    test_case.assertEqual(response.status, '200 OK')


def answer_question(test_case):
    expected_http_status = '200 OK'
    answer = 'This is very original answer'

    request_data = {"data": {"answer": answer}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['patch_question'], request_data)
    test_case.assertEqual(response.status, expected_http_status)

    # check answer
    response = test_case.app.get(test_case.ENTRYPOINTS['get_question'])
    question = response.json['data']
    test_case.assertEqual(question['answer'], answer)


def get_question(test_case):
    expected_http_status = '200 OK'

    response = test_case.app.get(test_case.ENTRYPOINTS['get_question'])

    test_case.assertEqual(response.status, expected_http_status)
