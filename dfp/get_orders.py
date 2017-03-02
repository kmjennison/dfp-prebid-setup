
from googleads import dfp

from dfp.client import get_client


def main():
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
  main()
