# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
    json_view,
    context_unpack
)
from openprocurement.auctions.core.views.mixins import AuctionBidResource
from openprocurement.auctions.core.validation import (
    validate_patch_bid_data
)
from openprocurement.auctions.core.interfaces import (
    IBidManager
)


@opresource(name='geb:Auction Bids',
            collection_path='/auctions/{auction_id}/bids',
            path='/auctions/{auction_id}/bids/{bid_id}',
            auctionsprocurementMethodType="geb",
            description="Auction bids")
class AuctionBidResource(AuctionBidResource):

    @json_view(content_type="application/json", permission='edit_bid', validators=(validate_patch_bid_data,))
    def patch(self):
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)

        if manager.change():
            manager.initialize()
            save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_bid_patch'})
            msg = 'Updated auction bid {}'.format(self.request.context.id)
            self.LOGGER.info(msg, extra=extra)
            return {'data': self.request.context.serialize(self.request.context.status)}

    @json_view(permission='edit_bid')
    def delete(self):
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)

        bid = manager.delete()
        if bid:
            save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_bid_delete'})
            msg = 'Deleted auction bid {}'.format(self.request.context.id)
            self.LOGGER.info(msg, extra=extra)
            return {'data': bid.serialize('view')}
