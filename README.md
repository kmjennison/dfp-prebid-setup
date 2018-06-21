[![Build Status](https://travis-ci.org/kmjennison/dfp-prebid-setup.svg?branch=master)](https://travis-ci.org/kmjennison/dfp-prebid-setup)

# DFP Setup Tool for Prebid
An automated DFP line item generator for [Prebid.js](http://prebid.org/)

## Overview
When setting up Prebid, your ad ops team often has to create [hundreds of line items](http://prebid.org/adops.html) in Doubleclick.

This tool automates setup for new header bidding partners. You define the advertiser, placements, and Prebid settings; then, it creates an order with one line item per price level, attaches creatives, and sets placement and Prebid key-value targeting.

While this tool covers typical use cases, it might not fit your needs. Check out the [limitations](#limitations) before you dive in.

## Getting Started

### Creating Google Credentials
_You will need credentials to access your DFP account programmatically. This summarizes steps from [DFP docs](https://developers.google.com/doubleclick-publishers/docs/authentication) and the DFP Python libary [auth guide](https://github.com/googleads/googleads-python-lib)._

1. If you haven't yet, sign up for a [DFP account](https://www.doubleclickbygoogle.com/solutions/revenue-management/dfp/).
2. Create Google developer credentials
   * Go to the [Google Developers Console Credentials page](https://console.developers.google.com/apis/credentials).
   * On the **Credentials** page, select **Create credentials**, then select **Service account key**.
   * Select **New service account**, and select JSON key type. You can leave the role blank.
   * Click **Create** to download a file containing a `.json` private key.
3. Enable API access to DFP
   * Sign into your [DFP account](https://www.google.com/dfp/). You must have admin rights.
   * In the **Admin** section, select **Global settings**
   * Ensure that **API access** is enabled.
   * Click the **Add a service account user** button.
     * Use the service account email for the Google developer credentials you created above.
     * Set the role to "Trafficker".
     * Click **Save**.

### Setting Up
1. Clone this repository.
2. Run `pip install -r requirements.txt`.
3. Rename key
   * Rename the Google credentials key you previously downloaded (`[something].json`) to `key.json` and move it to the root of this repository
4. Make a copy of `googleads.example.yaml` and name it `googleads.yaml`.
5. In `googleads.yaml`, set the required fields:
   * `application_name` is the name of the Google project you created when creating the service account credentials. It should appear in the top-left of the [credentials page](https://console.developers.google.com/apis/credentials).
   * `network_code` is your DFP network number; e.g., for `https://www.google.com/dfp/12398712#delivery`, the network code is `12398712`.

### Verifying Setup
Let's try it out! From the top level directory, run

`python -m dfp.get_orders`

and you should see all of the orders in your DFP account.

## Creating Line Items

Modify the following settings in `settings.py`:

Setting | Description | Type
------------ | ------------- | -------------
`DFP_ORDER_NAME` | What you want to call your new DFP order | string
`DFP_USER_EMAIL_ADDRESS` | The email of the DFP user who will be the trafficker for the created order | string
`DFP_ADVERTISER_NAME` | The name of the DFP advertiser for the created order | string
`DFP_TARGETED_PLACEMENT_NAMES` | The names of DFP placements the line items should target | array of strings
`DFP_PLACEMENT_SIZES` | The creative sizes for the targeted placements | array of objects (e.g., `[{'width': '728', 'height': '90'}]`)
`PREBID_BIDDER_CODE` | The value of [`hb_bidder`](http://prebid.org/dev-docs/publisher-api-reference.html#module_pbjs.bidderSettings) for this partner | string
`PREBID_PRICE_BUCKETS` | The [price granularity](http://prebid.org/dev-docs/publisher-api-reference.html#module_pbjs.setPriceGranularity); used to set `hb_pb` for each line item | object

Then, from the root of the repository, run:

`python -m tasks.add_new_prebid_partner`

You should be all set! Review your order, line items, and creatives to make sure they are correct. Then, approve the order in DFP.

*Note: DFP might show a "Needs creatives" warning on the order for ~15 minutes after order creation. Typically, the warning is incorrect and will disappear on its own.*

## Additional Settings

In most cases, you won't need to modify these settings.

Setting | Description | Default
------------ | ------------- | -------------
`DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST` | Whether we should create the advertiser with `DFP_ADVERTISER_NAME` in DFP if it does not exist | `False`
`DFP_USE_EXISTING_ORDER_IF_EXISTS` | Whether we should modify an existing order if one already exists with name `DFP_ORDER_NAME` | `False`
`DFP_NUM_CREATIVES_PER_LINE_ITEM` | The number of duplicate creatives to attach to each line item. Due to [DFP limitations](https://support.google.com/dfp_sb/answer/82245?hl=en), this should be equal to or greater than the number of ad units you serve on a given page. | the length of setting `DFP_TARGETED_PLACEMENT_NAMES`
`DFP_CURRENCY_CODE` | The currency to use in line items. | `'USD'`

## Limitations

* Currently, the names of the bidder code targeting key (`hb_bidder`) and price bucket targeting key (`hb_pb`) are not customizable. The `hb_bidder` targeting key is currently required (see [#18](../../issues/18))
* This tool does not support additional line item targeting beyond placement, `hb_bidder`, and `hb_pb` values. Placement targeting is currently required (see [#16](../../issues/16)), and targeting by ad unit isn't supported (see [#17](../../issues/17))
* The price bucketing setting `PREBID_PRICE_BUCKETS` only allows for uniform bucketing. For example, you can create $0.01 buckets from $0 - $20, but you cannot specify $0.01 buckets from $0 - $5 and $0.50 buckets from $5 - $20. Using entirely $0.01 buckets will still work for the custom buckets—you'll just have more line items than you need.
* This tool does not modify existing orders or line items, it only creates them. If you need to make a change to an order, it's easiest to archive the existing order and recreate it.

Please consider [contributing](CONTRIBUTING.md) to make the tool more flexible.

