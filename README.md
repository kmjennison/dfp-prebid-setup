# DFP Prebid Setup Tool
Quick, automated DFP line item generator for Prebid

## How to Use

### Creating Credentials
_This summarizes steps from [DFP docs](https://developers.google.com/doubleclick-publishers/docs/authentication) and the DFP Python libary [auth guide](https://github.com/googleads/googleads-python-lib)._

1. If you haven't yet, sign up for a [DFP account](https://www.doubleclickbygoogle.com/solutions/revenue-management/dfp/).
2. Create Google developer credentials
  * Go to the [Google Developers Console Credentials page](https://console.developers.google.com/apis/credentials).
  * On the **Credentials** page, select **Create credentials**, then select **Service account key**.
  * Select **New service account**, and select P12 key type.
  * Click **Create** to download a file containing a private key. Take note of the password (probably Google's default, "notasecret").
3. Enable API access to DFP
  * Sign into your DFP account in the DFP user interface. You must have admin rights.
  * Select the **Admin** tab.
  * Ensure that API access is enabled.
  * Click the **Add a service account user** button.
  * Use the service account email for the Google developer credentials you created above.
  * Click on the **Save** button. A message should appear, confirming the addition of your service account.

### Setting Up
1. Clone this repository.
2. Run `pip install -r requirements.txt`.
3. Convert the PKCS12 key format to PEM
  * Rename the `.p12` key from your developer credentials to `key.p12` and move it to the root of the repository
  * Run `openssl pkcs12 -in key.p12 -nodes -nocerts > key.pem`. Enter your password.
  * Delete `key.p12`.

... more to come.
