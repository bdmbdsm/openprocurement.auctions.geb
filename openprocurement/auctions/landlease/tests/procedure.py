# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.landlease.tests.base import (
    test_auction_data,
    BaseWebTest,
    # BaseAuctionWebTest,
)

from openprocurement.auctions.landlease.tests.blanks.procedure import (
    create_auction_common,
    create_auction,
    create_auction_invalid_required_fields,
    create_auction_invalid_unsupported_media_type,
    create_auction_invalid_unprocessable_entity_common,
    create_procurementMethod
)

from openprocurement.auctions.landlease.tests.blanks.fields import (
    create_invalid_minNumberOfQualifiedBids
)

from openprocurement.auctions.landlease.tests.specifications import (
    REQUIRED_SCHEME_DEFINITION
)

from openprocurement.auctions.landlease.tests.helpers import (
    get_specification_fields
)


class CreateAuctionResourceTest(BaseWebTest):
    initial_data = test_auction_data

    test_create_auction = snitch(create_auction)
    test_create_auction_common = snitch(create_auction_common)
    # test_create_auction_auto_genered_fields  TODO


class CreateInvalidAuctionResourceTest(BaseWebTest):
    initial_data = test_auction_data

    test_create_auction_invalid_required_fields = snitch(create_auction_invalid_required_fields)
    test_create_auction_invalid_unsupported_media_type = snitch(create_auction_invalid_unsupported_media_type)
    test_create_auction_invalid_unprocessable_entity_common = snitch(create_auction_invalid_unprocessable_entity_common)


class CreateAuctionWithInvalidFieldsTest(BaseWebTest):
    initial_data = test_auction_data

    test_procurementMethod = snitch(create_invalid_minNumberOfQualifiedBids)


class AuctionAutoGenereteFieldsTest(BaseWebTest):
    initial_data = test_auction_data

    def setUp(self):
        super(AuctionAutoGenereteFieldsTest, self).setUp()
        self.auto_generate_filds = get_specification_fields(REQUIRED_SCHEME_DEFINITION,
                                                            field_type='autogenerated')

    test_create_procurementMethod = snitch(create_procurementMethod)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateAuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')