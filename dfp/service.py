
from googleads import dfp

from settings import GOOGLEADS_YAML_FILE


def get_client():
  return dfp.DfpClient.LoadFromStorage(GOOGLEADS_YAML_FILE)

def get_all_orders():
  """
  Prints all orders in DFP.

  Returns:
      None
  """

  dfp_client = get_client()

  # Initialize appropriate service.
  order_service = dfp_client.GetService('OrderService', version='v201702')

  # Create a statement to select orders.
  statement = dfp.FilterStatement()

  # Retrieve a small amount of orders at a time, paging
  # through until all orders have been retrieved.
  while True:
    response = order_service.getOrdersByStatement(statement.ToStatement())
    print response
    if 'results' in response:
      for order in response['results']:
        # Print out some information for each order.
        print('Order with ID "%d" and name "%s" was found.\n' % (order['id'],
                                                                 order['name']))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']
