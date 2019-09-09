[![Build Status](https://travis-ci.org/kmjennison/dfp-prebid-setup.svg?branch=master)](https://travis-ci.org/kmjennison/dfp-prebid-setup)

# Setup Tool for Prebid and GAM (previously DFP)
An automated line item generator for [Prebid.js](http://prebid.org/) and Google Ad Manager (previously DFP)

## Overview
When setting up Prebid, your ad ops team often has to create [hundreds of line items](http://prebid.org/adops.html) in Google Ad Manager (GAM).

This tool automates setup for new header bidding partners. You define the advertiser, placements or ad units, and Prebid settings; then, it creates an order with one line item per price level, attaches creatives, sets placement and/or ad units, and Prebid key-value targeting.

While this tool covers typical use cases, it might not fit your needs. Check out the [limitations](#limitations) before you dive in.

_Note: Doubleclick for Publishers (DFP) was recently renamed to Google Ad Manager (GAM), so this repository may refer to GAM as DFP._

## Getting Started

### Requirements
* Python version >= 3.6 and a basic knowledge of Python
* Access to create a service account in the Google Developers Console
* Admin access to your Google Ad Manager account

### Creating Google Credentials
_You will need credentials to access your GAM account programmatically. This summarizes steps from [GAM docs](https://developers.google.com/ad-manager/docs/authentication) and the Google Ads Python libary [auth guide](https://github.com/googleads/googleads-python-lib)._

1. If you haven't yet, sign up for a [GAM account](https://admanager.google.com/).
2. Create Google developer credentials
   * Go to the [Google Developers Console Credentials page](https://console.developers.google.com/apis/credentials).
   * On the **Credentials** page, select **Create credentials**, then select **Service account key**.
   * Select **New service account**, and select JSON key type. You can leave the role blank.
   * Click **Create** to download a file containing a `.json` private key.
3. Enable API access to GAM
   * Sign into your [GAM account](https://admanager.google.com/). You must have admin rights.
   * In the **Admin** section, select **Global settings**
   * Ensure that **API access** is enabled.
   * Click the **Add a service account user** button.
     * Use the service account email for the Google developer credentials you created above.
     * Set the role to "Administrator".
     * Click **Save**.

### Setting Up
1. Clone this repository.
2. Install Python dependencies
   * Run `pip install -r requirements.txt`
   * **Important:** Python version 3.6 or higher is required.
3. Rename key
   * Rename the Google credentials key you previously downloaded (`[something].json`) to `key.json` and move it to the root of this repository
4. Make a copy of `googleads.example.yaml` and name it `googleads.yaml`.
5. In `googleads.yaml`, set the required fields:
   * `application_name` is the name of the Google project you created when creating the service account credentials. It should appear in the top-left of the [credentials page](https://console.developers.google.com/apis/credentials).
   * `network_code` is your GAM network number; e.g., for `https://admanager.google.com/12398712#delivery`, the network code is `12398712`.

### Verifying Setup
Let's try it out! From the top level directory, run

`python -m dfp.get_orders`

and you should see all of the orders in your GAM account.

## Creating Line Items

Modify the following settings in `settings.py`:

Setting | Description | Type
------------ | ------------- | -------------
`DFP_ORDER_NAME` | What you want to call your new GAM order | string
`DFP_USER_EMAIL_ADDRESS` | The email of the GAM user who will be the trafficker for the created order | string
`DFP_ADVERTISER_NAME` | The name of the GAM advertiser for the created order | string
`DFP_TARGETED_AD_UNIT_NAMES` | The names of GAM ad units the line items should target | array of strings
`DFP_TARGETED_PLACEMENT_NAMES` | The names of GAM placements the line items should target | array of strings
`DFP_PLACEMENT_SIZES` | The creative sizes for the targeted placements | array of objects (e.g., `[{'width': '728', 'height': '90'}]`)
`PREBID_BIDDER_CODE` | The value of [`hb_bidder`](http://prebid.org/dev-docs/publisher-api-reference.html#module_pbjs.bidderSettings) for this partner | string
`PREBID_PRICE_BUCKETS` | The [price granularity](http://prebid.org/dev-docs/publisher-api-reference.html#module_pbjs.setPriceGranularity); used to set `hb_pb` for each line item | object

Then, from the root of the repository, run:

`python -m tasks.add_new_prebid_partner`

You should be all set! Review your order, line items, and creatives to make sure they are correct. Then, approve the order in GAM.

*Note: GAM might show a "Needs creatives" warning on the order for ~15 minutes after order creation. Typically, the warning is incorrect and will disappear on its own.*

## Additional Settings

In most cases, you won't need to modify these settings.

Setting | Description | Default
------------ | ------------- | -------------
`DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST` | Whether we should create the advertiser with `DFP_ADVERTISER_NAME` in GAM if it does not exist | `False`
`DFP_USE_EXISTING_ORDER_IF_EXISTS` | Whether we should modify an existing order if one already exists with name `DFP_ORDER_NAME` | `False`
`DFP_NUM_CREATIVES_PER_LINE_ITEM` | The number of duplicate creatives to attach to each line item. Due to GAM limitations, this should be equal to or greater than the number of ad units you serve on a given page. | the length of setting `DFP_TARGETED_PLACEMENT_NAMES`
`DFP_CURRENCY_CODE` | The currency to use in line items. | `'USD'`
`DFP_LINE_ITEM_FORMAT` | The format for the line item names. | `u'{bidder_code}: HB ${price}'`

## Limitations

* This tool does not currently support run-of-network line items (see [#16](../../issues/16)). You must target line items to placements, ad units, or both.
* Currently, the names of the bidder code targeting key (`hb_bidder`) and price bucket targeting key (`hb_pb`) are not customizable. The `hb_bidder` targeting key is currently required (see [#18](../../issues/18))
* This tool does not support additional line item targeting beyond placement, ad units, `hb_bidder`, and `hb_pb` values. It does not yet support setting other options on the line item such as the "Allow same advertiser exception" (see [#59](../../issues/59))
* The price bucketing setting `PREBID_PRICE_BUCKETS` only allows for uniform bucketing (see [#27](../../issues/27)). For example, you can create $0.01 buckets from $0 - $20, but you cannot specify $0.01 buckets from $0 - $5 and $0.50 buckets from $5 - $20. Using entirely $0.01 buckets will still work for the custom buckets—you'll just have more line items than you need.
* This tool does not modify existing orders or line items, it only creates them. If you need to make a change to an order, it's easiest to archive the existing order and recreate it.

Please consider [contributing](CONTRIBUTING.md) to make the tool more flexible.

## Contributors
Thanks to these people for making this tool better 🤗:

[@couhie](https://github.com/couhie), [@dlackty](https://github.com/dlackty), [@pbrisson](https://github.com/pbrisson), [@jsonUK](https://github.com/jsonUK)
