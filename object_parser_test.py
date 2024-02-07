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

    # Define a test object with various data types
    test_object = {
  
  "farms": [
    {
          "farmId": { "unique": True, "value": "123lksjdfi-alskdjfi3-slakdjfljasldfj" },
          "farmRegistrationId": { "double_hash": True, "value": "FP-123234" },
          "someOtherValue": { "hash": True, "value": "alsdjfk" }
        }
      ]
    }

    # Call the parse_obj method with the test object
    response, unique = obj_parser.preprocess_obj(test_object)

    # Print the response
    print("Response from parse_obj:")
    print(json.dumps(response, indent=4))
    print(unique)
    
# Run the main function
if __name__ == "__main__":
    main()
