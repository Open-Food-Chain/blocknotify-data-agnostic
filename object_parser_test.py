# Import necessary modules
import re
import json
import binascii
import hashlib
from datetime import datetime
from object_parser import ObjectParser

# ObjectParser class definition goes here
# [Paste the ObjectParser class code here]

def main():
    # Create an instance of ObjectParser
    obj_parser = ObjectParser()

    true = True

    # Define a test object with various data types
    test_object = { 
    "test": {
        "recordType": {
            "value": "BATCH_REGISTRATION",
            "clear_text": true
        },
        "batchId": {
            "value": "#FARMER_NATIONAL_ID:NP-123456|#PURCHASE_DATE:01/16/2024",
            "double_hash": true,
            "unique": true
        },
        "buyerId": {
            "value": "aa903a24-e6d4-495d-b57c-7c9ebdf0a7c8",
            "clear_text": true
        },
        "buyer": {
            "value": "JK Cooperatives",
            "clear_text": true
        },
        "farmerId": {
            "value": "ad22e448-8fec-40f8-a943-3142f572c3e5",
            "clear_text": true
        },
        "farmerNationalId": {
            "value": "NP-123456",
            "double_hash": true,
            "lookup": true
        },
        "farmerFriendlyName": {
            "value": "manifoldcamera806",
            "clear_text": true
        },
        "purchasedAt": {
            "value": "01/16/2024",
            "clear_text": true
        },
        "quantity": {
            "value": 100,
            "clear_text": true
        },
        "quantityUnit": {
            "name": {
                "value": "Gram",
                "clear_text": true
            },
            "abbvr": {
                "value": "g",
                "clear_text": true
            }
        },
        "quality": {
            "value": "dry_grains_seeds",
            "clear_text": true
        },
        "moisture": {
            "value": 10,
            "clear_text": true
        },
        "varieties": [
            {
                "value": "CRIN TC-1",
                "clear_text": true
            }
        ],
        "cacaoType": {
            "value": "Organic",
            "clear_text": true
        },
        "isPremiumPaid": {
            "value": true,
            "clear_text": true
        }
    }
    }

    # Call the parse_obj method with the test object
    response = obj_parser.preprocess_save(test_object)

    # Print the response
    print("Response from parse_obj:")
    print(json.dumps(response, indent=4))


# Run the main function
if __name__ == "__main__":
    main()
