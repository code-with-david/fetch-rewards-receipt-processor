import unittest
from app import calculate_points

class TestCalculatePoints(unittest.TestCase):

    def test_alphanumeric_retailer(self):
        receipt = {
            "retailer": "Target123",
            "total": "0.10",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": []
        }
        self.assertEqual(calculate_points(receipt), 9)  # 9 alphanumeric characters

    def test_round_dollar_total(self):
        receipt = {
            "retailer": "Store",
            "total": "10.00",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": []
        }
        self.assertEqual(calculate_points(receipt), 80)  # 5 alphanumeric + 50 for round dollar + 25 for total is a multiple of 0.25

    def test_multiple_of_0_25(self):
        receipt = {
            "retailer": "Shop",
            "total": "0.25",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": []
        }
        self.assertEqual(calculate_points(receipt), 29)  # 4 alphanumeric + 25 for multiple of 0.25

    def test_items_points(self):
        receipt = {
            "retailer": "Market",
            "total": "0.30",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Item1", "price": "1.00"},
                      {"shortDescription": "Item2", "price": "1.00"}]
        }
        self.assertEqual(calculate_points(receipt), 11)  # 6 alphanumeric + 5 for two items

    def test_item_description_length(self):
        receipt = {
            "retailer": "Store",
            "total": "0.30",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "abc", "price": "5.00"}]
        }
        self.assertEqual(calculate_points(receipt), 6)  # 5 alphanumeric + 1 point for description length

    def test_odd_day(self):
        receipt = {
            "retailer": "Shop",
            "total": "0.30",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": []
        }
        self.assertEqual(calculate_points(receipt), 10)  # 4 alphanumeric + 6 for odd day

    def test_time_of_purchase(self):
        receipt = {
            "retailer": "Store",
            "total": "0.30",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "14:30",
            "items": []
        }
        self.assertEqual(calculate_points(receipt), 15)  # 5 alphanumeric + 10 for time
      
    def test_sample_1(self):
        receipt = {
          "retailer": "Target",
          "purchaseDate": "2022-01-01",
          "purchaseTime": "13:01",
          "items": [
            {
              "shortDescription": "Mountain Dew 12PK",
              "price": "6.49"
            },{
              "shortDescription": "Emils Cheese Pizza",
              "price": "12.25"
            },{
              "shortDescription": "Knorr Creamy Chicken",
              "price": "1.26"
            },{
              "shortDescription": "Doritos Nacho Cheese",
              "price": "3.35"
            },{
              "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
              "price": "12.00"
            }
          ],
          "total": "35.35"
        }
        self.assertEqual(calculate_points(receipt), 28)

    def test_sample_2(self):
        receipt = {
          "retailer": "M&M Corner Market",
          "purchaseDate": "2022-03-20",
          "purchaseTime": "14:33",
          "items": [
            {
              "shortDescription": "Gatorade",
              "price": "2.25"
            },{
              "shortDescription": "Gatorade",
              "price": "2.25"
            },{
              "shortDescription": "Gatorade",
              "price": "2.25"
            },{
              "shortDescription": "Gatorade",
              "price": "2.25"
            }
          ],
          "total": "9.00"
        }
        self.assertEqual(calculate_points(receipt), 109)

if __name__ == '__main__':
    unittest.main()