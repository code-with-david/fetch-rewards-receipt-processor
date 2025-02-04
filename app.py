from flask import Flask, request, jsonify
import uuid
import math
from datetime import datetime

app = Flask(__name__)

# In-memory storage for receipts
receipts = {}

def calculate_points(receipt):
    points = 0
    # Calculate points based on the rules
    retailer = receipt['retailer']
    total = float(receipt['total'])
    purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M')
    items = receipt['items']

    # Rule 1: One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in retailer)

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    points += (len(items) // 2) * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer.
    for item in items:
        description_length = len(item['shortDescription'].strip())
        if description_length % 3 == 0:
            item_price = float(item['price'])
            points += math.ceil(item_price * 0.2)  # Round up

    # Rule 7: 6 points if the day in the purchase date is odd
    if purchase_date.day % 2 != 0:
        points += 6

    # Rule 8: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    if 14 <= purchase_time.hour < 16:
        points += 10

    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.json
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts[receipt_id] = points
    return jsonify({"id": receipt_id}), 200

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    if receipt_id in receipts:
        return jsonify({"points": receipts[receipt_id]}), 200
    else:
        return jsonify({"error": "No receipt found for that ID."}), 404

if __name__ == '__main__':
    app.run(debug=True) 