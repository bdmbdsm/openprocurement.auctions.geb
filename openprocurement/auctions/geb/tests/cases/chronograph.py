# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    test_auction_data,
    BaseAuctionWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    Procedure
)

from openprocurement.auctions.geb.tests.helpers import (
    get_procedure_state
)


from openprocurement.auctions.geb.tests.blanks.chronograph import (
    check_tender_period_end_no_active_bids,
    check_tender_period_end_no_minNumberOfQualifiedBids,
    check_tender_period_end_successful,
    check_enquiry_period_end_unsuccessful,
    check_enquiry_period_end_active_auction,
    check_enquiry_period_end_active_qualification,
    check_rectification_period_end,
    check_enquiry_period_end_set_unsuccessful_bids
)


class ChronographRectificationTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_check_rectification_period_end = snitch(check_rectification_period_end)

    def setUp(self):
        super(ChronographRectificationTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.rectification')
        entrypoints = {}
        self.auction = state.auction
        self.app.authorization = ('Basic', ('chronograph', ''))

        entrypoints['auction'] = '/auctions/{}'.format(self.auction_id)
        self.ENTRYPOINTS = entrypoints


class ChronographTenderingTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_no_active_bids = snitch(check_tender_period_end_no_active_bids)
    test_no_minNumberOfQualifiedBids = snitch(check_tender_period_end_no_minNumberOfQualifiedBids)
    test_successful = snitch(check_tender_period_end_successful)

    def setUp(self):
        super(ChronographTenderingTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.tendering')
        entrypoints = {}
        self.auction = state.auction
        self.app.authorization = ('Basic', ('chronograph', ''))

        entrypoints['auction'] = '/auctions/{}'.format(self.auction_id)
        self.ENTRYPOINTS = entrypoints


class ChronographEnquiryTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_unsuccessful = snitch(check_enquiry_period_end_unsuccessful)
    test_active_auction = snitch(check_enquiry_period_end_active_auction)
    test_active_qualification = snitch(check_enquiry_period_end_active_qualification)
    test_check_set_unsuccessful_bids = snitch(check_enquiry_period_end_set_unsuccessful_bids)

    def setUp(self):
        super(ChronographEnquiryTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'active.enquiry')
        entrypoints = {}
        self.auction = state.auction
        self.extra = state.extra
        self.app.authorization = ('Basic', ('chronograph', ''))

        entrypoints['auction'] = '/auctions/{}'.format(self.auction_id)
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ChronographRectificationTest))
    suite.addTest(unittest.makeSuite(ChronographTenderingTest))
    suite.addTest(unittest.makeSuite(ChronographEnquiryTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
