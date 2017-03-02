"""
This example gets all orders.
"""

# Import appropriate modules from the client library.
from googleads import dfp

from settings import GOOGLEADS_YAML_FILE

def main(client):
  # Initialize appropriate service.
  order_service = client.GetService('OrderService', version='v201702')

  # Create a statement to select orders.
  statement = dfp.FilterStatement()

  # Retrieve a small amount of orders at a time, paging
  # through until all orders have been retrieved.
  while True:
    response = order_service.getOrdersByStatement(statement.ToStatement())
    if 'results' in response:
      for order in response['results']:
        # Print out some information for each order.
        print('Order with ID "%d" and name "%s" was found.\n' % (order['id'],
                                                                 order['name']))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage(GOOGLEADS_YAML_FILE)
  main(dfp_client)
