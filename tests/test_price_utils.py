
from unittest import TestCase

from tasks.price_utils import (
  num_to_micro_amount,
  num_to_str,
  get_prices_array,
  get_prices_summary_string,
  micro_amount_to_num,
)


class UtilsTests(TestCase):

  def test_num_to_micro_amount(self):
    """
    It returns the expected conversion.
    """
    self.assertEqual(num_to_micro_amount(40), 40000000)
    self.assertEqual(num_to_micro_amount(5), 5000000)
    self.assertEqual(num_to_micro_amount(5.00), 5000000)
    self.assertEqual(num_to_micro_amount(40, precision=4), 40000000)
    self.assertEqual(num_to_micro_amount(5, precision=5), 5000000)
    self.assertEqual(num_to_micro_amount(5.01, precision=1), 5000000)
    self.assertEqual(num_to_micro_amount(3.12, precision=1), 3100000)
    self.assertEqual(num_to_micro_amount(0.10), 100000)
    self.assertEqual(num_to_micro_amount(0.10001), 100000)
    self.assertEqual(num_to_micro_amount(0.01), 10000)
    self.assertEqual(num_to_micro_amount(0.001), 0)
    self.assertEqual(num_to_micro_amount(0.001, precision=3), 1000)
    self.assertEqual(num_to_micro_amount(0.00043), 0)
    self.assertEqual(num_to_micro_amount(0.00043, precision=4), 400)
    self.assertEqual(num_to_micro_amount(0.00043, precision=5), 430)
    self.assertEqual(num_to_micro_amount(0), 0)

  def test_micro_amount_to_num(self):
    """
    It returns the expected conversion.
    """
    self.assertEqual(micro_amount_to_num(40000000), 40.0)
    self.assertEqual(micro_amount_to_num(5000000), 5.0)
    self.assertEqual(micro_amount_to_num(100000), 0.10)
    self.assertEqual(micro_amount_to_num(50000), 0.05)
    self.assertEqual(micro_amount_to_num(10000), 0.01)
    self.assertEqual(micro_amount_to_num(1000), 0.001)
    self.assertEqual(micro_amount_to_num(0), 0.0)

  def test_num_to_str(self):
    """
    It returns the expected conversion.
    """
    self.assertEqual(num_to_str(40), '40.00')
    self.assertEqual(num_to_str(5, precision=6), '5.000000')
    self.assertEqual(num_to_str(5.00), '5.00')
    self.assertEqual(num_to_str(0.10), '0.10')
    self.assertEqual(num_to_str(0.05533, precision=4), '0.0553')
    self.assertEqual(num_to_str(0.05533, precision=2), '0.06')
    self.assertEqual(num_to_str(0.01000012), '0.01')
    self.assertEqual(num_to_str(0.001, precision=3), '0.001')
    self.assertEqual(num_to_str(0.00043, precision=5), '0.00043')
    self.assertEqual(num_to_str(0), '0.00')

  def test_get_prices_array_normal(self):
    """
    It returns the expected array with normal use.
    """

    config = {
      'precision': 2,
      'min' : 0,
      'max' : 5,
      'increment': 0.50,
    }
    self.assertEqual(
      get_prices_array(config),
      [0, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 
        4000000, 4500000, 5000000]
    )

    config = {
      'precision': 2,
      'min' : 2,
      'max' : 3.50,
      'increment': 0.10,
    }
    self.assertEqual(
      get_prices_array(config),
        [2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000,
          2700000, 2800000, 2900000, 3000000, 3100000, 3200000, 3300000,
          3400000, 3500000]
    )

  def test_get_prices_array_changed_precision(self):
    """
    It returns the expected array with custom price precision.
    """

    config = {
      'precision': 3,
      'min' : 1,
      'max' : 1.1,
      'increment': 0.012,
    }
    self.assertEqual(
      get_prices_array(config),
        [1000000, 1012000, 1024000, 1036000, 1048000, 1060000, 1072000,
          1084000, 1096000]
    )

    config = {
      'precision': 2,
      'min' : 1,
      'max' : 1.1,
      'increment': 0.012,
    }
    self.assertEqual(
      get_prices_array(config),
        [1000000, 1010000, 1020000, 1030000, 1040000, 1050000, 1060000,
          1070000, 1080000, 1090000, 1100000]
    )

  def test_get_prices_array_length(self):
    """
    It returns the expected number of prices.
    """

    config = {
      'precision': 2,
      'min' : 0,
      'max' : 20,
      'increment': 0.10,
    }
    self.assertEqual(len(get_prices_array(config)), 201)

    config = {
      'precision': 2,
      'min' : 0,
      'max' : 20,
      'increment': 0.50,
    }
    self.assertEqual(len(get_prices_array(config)), 41)

    config = {
      'precision': 2,
      'min' : 0,
      'max' : 15,
      'increment': 0.01,
    }
    self.assertEqual(len(get_prices_array(config)), 1501)

  def test_get_prices_summary_string(self):
    """
    It returns the expected string summary of the array.
    """

    self.assertEqual(
      get_prices_summary_string([0, 500000, 1000000, 1500000, 2000000,
        2500000, 3000000, 3500000, 4000000, 4500000, 5000000]),
      '0.00, 0.50, 1.00, ... 4.00, 4.50, 5.00'
    )

    # Short array
    self.assertEqual(
      get_prices_summary_string([3200000, 3300000, 3400000, 3500000]),
      '3.20, 3.30, 3.40, 3.50'
    )
  