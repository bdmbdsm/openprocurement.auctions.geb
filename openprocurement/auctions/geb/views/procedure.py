# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    context_unpack,
    json_view,
    opresource
)
from openprocurement.auctions.core.views.mixins import (
    AuctionResource
)
from openprocurement.auctions.core.interfaces import (
    IManager
)
from openprocurement.auctions.geb.validation import (
    validate_patch_resource_data
)


@opresource(name='geb:Auction', path='/auctions/{auction_id}', auctionsprocurementMethodType="geb")
class AuctionResource(AuctionResource):

    @json_view(content_type="application/json",
               validators=(validate_patch_resource_data,),
               permission='edit_auction')
    def patch(self):
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IManager)

        manager.change()
        save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_patch'})
            self.LOGGER.info('Updated auction {}'.format(self.context.id), extra=extra)
            return {'data': self.context.serialize(self.context.status)}
