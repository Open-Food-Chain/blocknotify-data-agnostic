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
    "recordType": {
        "value": "FARMER_REGISTRATION",
        "clear_text": true
    },
    "farmerId": {
        "value": "ad22e448-8fec-40f8-a943-3142f572c3e5",
        "unique": true,
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
    "farms": [
        {
            "farmId": {
                "value": "b8a34d88-c8f6-4e51-a476-d10258fab291",
                "clear_text": true
            },
            "farmRegistrationId": {
                "value": "AR_01",
                "double_hash": true
            },
            "lat": 87.24,
            "lng": 27.85,
            "geofenceCoordinates": [
                {
                    "lat": 88.24,
                    "lng": 27.5
                },
                {
                    "lat": 88.24,
                    "lng": 28.5
                },
                {
                    "lat": 87.24,
                    "lng": 28.5
                },
                {
                    "lat": 87.24,
                    "lng": 27.5
                }
            ],
            "polygonalZones": [
                {
                    "zoneId": {
                        "value": "a4358dc9-ae05-45ad-88c3-e7d4a1fad050",
                        "clear_text": true
                    },
                    "polygonCoordinates": [
                        {
                            "lat": 87.24,
                            "lng": 27.5
                        },
                        {
                            "lat": 87.24,
                            "lng": 28.5
                        },
                        {
                            "lat": 88.24,
                            "lng": 28.5
                        },
                        {
                            "lat": 88.24,
                            "lng": 27.5
                        }
                    ]
                }
            ],
            "deforestationReports": {
                "reportGuid": {
                    "value": "cef04d73-a7fa-4318-8146-159d5c74cf6a",
                    "clear_text": true
                },
                "transactionHash": {
                    "value": "0xffa70c37b1fdcad6d5485f05e9d60c2c327a666804b0b469e5d5df538c3e5bf8",
                    "clear_text": true
                },
                "keccakHash": {
                    "value": "0x55c68e8a3c3d614ff930698c1f290d1d61635de9c93aed4aa0302aaca886da25",
                    "clear_text": true
                },
                "center": {
                    "lat": -11.32145447649449,
                    "lng": -75.34963488578796
                },
                "status": {
                    "value": "CERTIFICATE_READY",
                    "clear_text": true
                },
                "reportType": {
                    "value": "REGISTERED_FARM",
                    "clear_text": true
                },
                "requestedAt": {
                    "value": "2024-01-16T06:59:02.000Z",
                    "clear_text": true
                },
                "isCertified": {
                    "value": true,
                    "clear_text": true
                },
                "highProbabilityArea": {
                    "value": 0.964321,
                    "clear_text": true
                },
                "highProbabilityPercent": {
                    "value": 0.0490741,
                    "clear_text": true
                },
                "lowProbabilityArea": {
                    "value": 14.5917,
                    "clear_text": true
                },
                "zeroProbabilityArea": {
                    "value": 1949.48,
                    "clear_text": true
                },
                "zeroProbabilityPercent": {
                    "value": 99.2084,
                    "clear_text": true
                },
                "totalArea": {
                    "value": 1965.03,
                    "clear_text": true
                },
                "overallProb": {
                    "value": "Low Deforestation Probability",
                    "clear_text": true
                }
            }
        }
    ]
}

    # Call the parse_obj method with the test object
    response = obj_parser.preprocess_save(test_object)

    # Print the response
    print("Response from parse_obj:")
    print(json.dumps(response, indent=4))


# Run the main function
if __name__ == "__main__":
    main()
