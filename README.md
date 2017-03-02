# DFP Prebid Setup Tool
Quick, automated DFP line item generator for [Prebid.js](http://prebid.org/)

## Overview
When setting up Prebid, your ad ops team often has to create [hundreds of line items](http://prebid.org/adops.html) in Doubleclick.

This project automates line item creation for new header bidding partners. It aims to solve the typical use case: one order per header bidding partner, one line item per price bucket, and standard Prebid key-value targeting.

## Getting Started

### Creating Google Credentials
_You will need credentials to access your DFP account programmatically. This summarizes steps from [DFP docs](https://developers.google.com/doubleclick-publishers/docs/authentication) and the DFP Python libary [auth guide](https://github.com/googleads/googleads-python-lib)._

1. If you haven't yet, sign up for a [DFP account](https://www.doubleclickbygoogle.com/solutions/revenue-management/dfp/).
2. Create Google developer credentials
  * Go to the [Google Developers Console Credentials page](https://console.developers.google.com/apis/credentials).
  * On the **Credentials** page, select **Create credentials**, then select **Service account key**.
  * Select **New service account**, and select P12 key type.
  * Click **Create** to download a file containing a `.p12` private key. Take note of the password (probably Google's default, "notasecret").
3. Enable API access to DFP
  * Sign into your [DFP account](https://www.google.com/dfp/). You must have admin rights.
  * Select the **Admin** tab.
  * Ensure that API access is enabled.
  * Click the **Add a service account user** button.
  * Use the service account email for the Google developer credentials you created above.
  * Click on the **Save** button. A message should appear, confirming the addition of your service account.

### Setting Up
1. Clone this repository.
2. Run `pip install -r requirements.txt`.
3. Convert the PKCS12 key format to PEM
  * Rename the Google credentials key you previously downloaded (`[something].p12`) to `key.p12` and move it to the root of this repository
  * Run `openssl pkcs12 -in key.p12 -nodes -nocerts > key.pem`. Enter your password.
  * Delete `key.p12`.
4. Make a copy of `googleads.example.yaml` and name it `googleads.yaml`.
5. In `googleads.yaml`, set the required fields:
  * `application_name` is the name of the application you set up for your Google developer credentials
  * `network_code` is your DFP network number; e.g., for `https://www.google.com/dfp/12398712#delivery`, the network code is `12398712`.
  * `service_account_email` is the account email for the Google developer credentials

### Verifying Setup
Let's try it out! From the top level directory, run

`python -m dfp.get_orders`

and you should see all of the orders in your DFP account.

## Creating Prebid Line Items

... more to come.
