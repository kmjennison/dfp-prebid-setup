
from unittest import TestCase
from mock import MagicMock, patch

import settings
import dfp.create_line_items
from dfp.exceptions import BadSettingException, MissingSettingException


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPCreateLineItemsTests(TestCase):

  def test_create_line_items_call(self, mock_dfp_client):
    """
    Ensure it calls DFP once with line item info.
    """

    mock_dfp_client.return_value = MagicMock()

    line_items_config = [
      dfp.create_line_items.create_line_item_config(name='My Line Item', order_id=1234567,
                                                    placement_ids=['one-placement', 'another-placement'],
                                                    ad_unit_ids=['ad-unit', 'anoher-ad-unit'], cpm_micro_amount=10000000, sizes=[],
                                                    hb_bidder_key_id=999999, hb_pb_key_id=888888,
                                                    hb_bidder_value_id=222222, hb_pb_value_id=111111)
    ]

    dfp.create_line_items.create_line_items(line_items_config)

    (mock_dfp_client.return_value
      .GetService.return_value
      .createLineItems.assert_called_once_with(line_items_config)
      )

  def test_create_line_item_config(self, mock_dfp_client):
    """
    Ensure the line item config is created as expected.
    """

    self.assertEqual(
      dfp.create_line_items.create_line_item_config(name='A Fake Line Item', order_id=1234567,
                                                    placement_ids=['one-placement', 'another-placement-id'],
                                                    ad_unit_ids=['ad-unit', 'anoher-ad-unit'], cpm_micro_amount=24000000, sizes=[{
          'width': '728',
          'height': '90',
        }], hb_bidder_key_id=999999, hb_pb_key_id=888888, hb_bidder_value_id=222222, hb_pb_value_id=111111),
      {
        'orderId': 1234567,
        'startDateTimeType': 'IMMEDIATELY',
        'targeting': {
          'inventoryTargeting': {
            'targetedAdUnits': [{'adUnitId': 'ad-unit'}, {'adUnitId': 'anoher-ad-unit'}],
            'targetedPlacementIds': ['one-placement', 'another-placement-id']
          },
          'customTargeting': {
            'children': [
              {
                'keyId': 999999,
                'operator': 'IS',
                'valueIds': [222222],
                'xsi_type': 'CustomCriteria'
              },
              {
                'keyId': 888888,
                'operator': 'IS',
                'valueIds': [111111],
                'xsi_type': 'CustomCriteria'
              }
            ],
            'logicalOperator': 'AND',
            'xsi_type': 'CustomCriteriaSet'
          },
        },
        'name': 'A Fake Line Item',
        'costType': 'CPM',
        'costPerUnit': {'currencyCode': 'USD', 'microAmount': 24000000},
        'creativeRotationType': 'EVEN',
        'lineItemType': 'PRICE_PRIORITY',
        'unlimitedEndDateTime': True,
        'primaryGoal': {
          'goalType': 'NONE'
        },
        'creativePlaceholders': [
          {
            'size': {
              'width': '728',
              'height': '90'
            }
          },
        ],
      }
    )

    # Change some inputs.
    self.assertEqual(
      dfp.create_line_items.create_line_item_config(name='Cool Line Item', order_id=22334455,
                                                    placement_ids=['one-placement', 'another-placement-id'],
                                                    ad_unit_ids=['ad-unit', 'anoher-ad-unit'], cpm_micro_amount=40000000, sizes=[{
          'width': '728',
          'height': '90',
        }], hb_bidder_key_id=999999, hb_pb_key_id=888888, hb_bidder_value_id=222222, hb_pb_value_id=111111,
                                                    currency_code='EUR'),
      {
        'orderId': 22334455,
        'startDateTimeType': 'IMMEDIATELY',
        'targeting': {
          'inventoryTargeting': {
            'targetedAdUnits': [{'adUnitId': 'ad-unit'}, {'adUnitId': 'anoher-ad-unit'}],
            'targetedPlacementIds': ['one-placement', 'another-placement-id']
          },
          'customTargeting': {
            'children': [
              {
                'keyId': 999999,
                'operator': 'IS',
                'valueIds': [222222],
                'xsi_type': 'CustomCriteria'
              },
              {
                'keyId': 888888,
                'operator': 'IS',
                'valueIds': [111111],
                'xsi_type': 'CustomCriteria'
              }
            ],
            'logicalOperator': 'AND',
            'xsi_type': 'CustomCriteriaSet'
          },
        },
        'name': 'Cool Line Item',
        'costType': 'CPM',
        'costPerUnit': {'currencyCode': 'EUR', 'microAmount': 40000000},
        'creativeRotationType': 'EVEN',
        'lineItemType': 'PRICE_PRIORITY',
        'unlimitedEndDateTime': True,
        'primaryGoal': {
          'goalType': 'NONE'
        },
        'creativePlaceholders': [
          {
            'size': {
              'width': '728',
              'height': '90'
            }
          },
        ],
      }
    )

    # With video ad type
    self.assertEqual(
      dfp.create_line_items.create_line_item_config(name='Video Line Item', order_id=42,
                                                    placement_ids=['video-placement'],
                                                    ad_unit_ids=['video-ad-unit'], cpm_micro_amount=40000000, sizes=[{
          'width': '640',
          'height': '480',
        }], hb_bidder_key_id=999999, hb_pb_key_id=888888, hb_bidder_value_id=222222, hb_pb_value_id=111111,
                                                    currency_code='EUR', video_ad_type=True),
      {
        'orderId': 42,
        'startDateTimeType': 'IMMEDIATELY',
        'targeting': {
          'inventoryTargeting': {
            'targetedAdUnits': [{'adUnitId': 'video-ad-unit'}],
            'targetedPlacementIds': ['video-placement']
          },
          'customTargeting': {
            'children': [
              {
                'keyId': 999999,
                'operator': 'IS',
                'valueIds': [222222],
                'xsi_type': 'CustomCriteria'
              },
              {
                'keyId': 888888,
                'operator': 'IS',
                'valueIds': [111111],
                'xsi_type': 'CustomCriteria'
              }
            ],
            'logicalOperator': 'AND',
            'xsi_type': 'CustomCriteriaSet'
          },
          'requestPlatformTargeting': ({'targetedRequestPlatforms': ['VIDEO_PLAYER']},),
        },
        'name': 'Video Line Item',
        'costType': 'CPM',
        'costPerUnit': {'currencyCode': 'EUR', 'microAmount': 40000000},
        'creativeRotationType': 'EVEN',
        'environmentType': 'VIDEO_PLAYER',
        'lineItemType': 'PRICE_PRIORITY',
        'unlimitedEndDateTime': True,
        'primaryGoal': {
          'goalType': 'NONE'
        },
        'creativePlaceholders': [
          {
            'size': {
              'width': '640',
              'height': '480'
            }
          },
        ],
      }
    )

  def test_create_line_items_returns_ids(self, mock_dfp_client):
    """
    Ensure it returns the IDs of created line items.
    """

    # Mock DFP response after creating line items.
    (mock_dfp_client.return_value
      .GetService.return_value
      .createLineItems) = MagicMock(return_value=[
        
        # Approximate shape of DFP line item response.
        {
          'orderId': 8675309,
          'id': 16273849,
          'name': 'Some Advertiser HB $2.50',
          'orderName': 'My Example Test Order',
          'startDateTime': {},
          'startDateTimeType': 'USE_START_DATE_TIME',
          'autoExtensionDays': 0,
          'unlimitedEndDateTime': True,
          'creativeRotationType': 'EVEN',
          'deliveryRateType': 'FRONTLOADED',
          'roadblockingType': 'ONE_OR_MORE',
          'lineItemType': 'PRICE_PRIORITY',
          'priority': 12,
          'costPerUnit': {
            'currencyCode': 'USD',
            'microAmount': 2500000,
          },
          'valueCostPerUnit': {
            'currencyCode': 'USD',
            'microAmount': 0,
          },
          'costType': 'CPM',
          'discountType': 'PERCENTAGE',
          'discount': 0.0,
          'contractedUnitsBought': 0,
          'creativePlaceholders': [
            {
              'expectedCreativeCount': 1,
              'creativeSizeType': 'PIXEL',
            },
          ],
          'environmentType': 'BROWSER',
          'companionDeliveryOption': 'UNKNOWN',
          'creativePersistenceType': 'NOT_PERSISTENT',
          'allowOverbook': False,
          'skipInventoryCheck': False,
          'skipCrossSellingRuleWarningChecks': False,
          'reserveAtCreation': False,
          'budget': {
            'currencyCode': 'USD',
            'microAmount': 0,
          },
          'status': 'DRAFT',
          'reservationStatus': 'UNRESERVED',
          'isArchived': False,
          'webPropertyCode': None,
          'disableSameAdvertiserCompetitiveExclusion': False,
          'lastModifiedByApp': 'some-app',
          'lastModifiedDateTime': {},
          'creationDateTime': {},
          'isPrioritizedPreferredDealsEnabled': False,
          'adExchangeAuctionOpeningPriority': 0,
          'isSetTopBoxEnabled': False,
          'isMissingCreatives': False,
          'videoMaxDuration': 0,
          'primaryGoal': {
            'goalType': 'NONE',
            'unitType': 'IMPRESSIONS',
            'units': -1,
          },
          'targeting': {
          'inventoryTargeting': {
            'targetedPlacementIds': [123456, 7891011],
            'technologyTargeting': '',
            }
          }
        },
        # Some simple mock line items.
        {
          'id': 444555666,
        },
        {
          'id': 999888777,
        },
      ])

    line_items_config = [{}, {}] # Mock does not matter.
    self.assertEqual(
      dfp.create_line_items.create_line_items(line_items_config),
      [16273849, 444555666, 999888777]
    )

