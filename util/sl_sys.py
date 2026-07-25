
from typing import Any

import json
import os

# Saving functionality
def save(text, f) -> None:
    '''
    Save to a JSON file from a dictionary.

    :param text: The dictionary to save to the specified file.
    :param f: The file to write to.

    :type text: dict
    :type f: str

    > **Warning:** This will overwrite the file, or create a new file in the current directory.
    '''

    # Dump dictionary to a JSON file
    with open(f, 'w') as file:
        json.dump(text, file, indent=2)

# Loading functionality
def load(f: str) -> dict:
    '''
    Loads a JSON file to a dictionary.

    :param f: The file to read from.

    :type f: str

    :return: Dictionary of JSON file.

    :rtype: dict

    :raises FileNotFoundError: If the file cannot be found at the given location.
    '''

    # Check if the file exists
    if not os.path.exists(f):
        # [;] Could not find the file: failure
        raise FileNotFoundError("File was not found at the given location.")

    # Read the file and return as a dictionary
    with open(f, 'r') as file:
        return json.load(file)

# Modify a specific key
def modify_nested(keys: list[Any], new: Any, f: str) -> str:
    '''
    Can update a key at any depth in JSON.

    :param keys: A *list* of keys leading to the target key.
    :param new: The value to update the targeted key/value with.
    :param f: The file to read and write to.

    :type keys: list
    :type new: arr | int | str | float | dict
    :type f: str

    :return: String "Success"

    :rtype: str

    :raises FileNotFoundError: If the file cannot be found at the given location.
    :raises Exception: Such as KeyError, TypeError, or FileNotFoundError when writing the change.

    > **Warning:** This will modify a key in the targeted file.
    '''

    # 1. CHECK IF FILE EXISTS
    if os.path.exists(f):
        with open(f, 'r') as file:
            data = json.load(file)
    else:
        # Return error
        raise FileNotFoundError("File was not found at the given location.")

    # 2. LOCATE AND UPDATE DATA POINT
    current_depth = data
    try:
        # Loop through key list and navigate through JSON file
        for key in keys[:-1]:
            current_depth = current_depth[key]

        # Once the target key has been found, add it to a variable
        final = keys[-1]
        # Set the value of the target key
        current_depth[final] = new
    except(KeyError, TypeError, FileNotFoundError) as e:
        # [;] Return error if failure
        return f"{e}"

    # 3. REWRITE JSON FILE WITH NEW DATA USING TEMP FILE
    # Create and dump to temp file
    # INFO: Temp file prevents data loss
    temp_name = f + '.tmp'
    with open(temp_name, 'w') as file:
        json.dump(data, file, indent=2)
    # Replace old main file with new temp file
    os.replace(temp_name, f)

    # [!] 4. RETURN SUCCESSFUL MODIFICATION
    return 'Success'

