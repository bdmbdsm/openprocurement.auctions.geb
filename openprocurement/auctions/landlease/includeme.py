import os
import logging
from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import (
    IContentConfigurator,
    IAwardingNextCheck,
    get_evenly_plugins
)
from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingNextCheckV2_1
)

from openprocurement.auctions.landlease.adapters import (
    AuctionLandLeaseConfigurator,
    AuctionLandLeaseManagerAdapter,
)
from openprocurement.auctions.landlease.constants import (
    DEFAULT_LEVEL_OF_ACCREDITATION,
    DEFAULT_PROCUREMENT_METHOD_TYPE,
)
from openprocurement.auctions.landlease.models import (
    ILandLeaseAuction,
    LandLease,
)

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_map):
    procurement_method_types = plugin_map.get('aliases', [])
    if plugin_map.get('use_default', False):
        procurement_method_types.append(
            DEFAULT_PROCUREMENT_METHOD_TYPE
        )
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(LandLease,
                                                 procurementMethodType)

    config.scan("openprocurement.auctions.landlease.views")

    # Register adapters
    config.registry.registerAdapter(
        AuctionLandLeaseConfigurator,
        (ILandLeaseAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AwardingNextCheckV2_1,
        (ILandLeaseAuction,),
        IAwardingNextCheck
    )
    config.registry.registerAdapter(
        AuctionLandLeaseManagerAdapter,
        (ILandLeaseAuction,),
        IAuctionManager
    )

    LOGGER.info("Included openprocurement.auctions.landlease plugin",
                extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_map.get('accreditation'):
        config.registry.accreditation['auction'][LandLease._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['auction'][LandLease._internal_type] = plugin_map['accreditation']

    # migrate data
    if plugin_map['migration'] and not os.environ.get('MIGRATION_SKIP'):
        get_evenly_plugins(config, plugin_map['plugins'], 'openprocurement.auctions.landlease.plugins')