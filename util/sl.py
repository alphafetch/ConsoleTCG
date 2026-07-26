from typing import Any

import tomlkit as tmlk
import os

# Saving functionality
def save(data, f) -> None:
    '''
    Save to a TOML file from a dictionary.

    :param data: The dictionary to save to the specified file.
    :param f: The file to write to.

    :type data: dict
    :type f: str

    > **Warning:** This will overwrite the file, or create a new file in the current directory.
    '''

    # Dump dictionary to a TOML file
    if os.path.exists(f):
        with open(f, 'w') as file:
            file.write(tmlk.dumps(data))
    else:
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w") as file:
            file.write(tmlk.dumps(data))

# Loading functionality
def load(f: str) -> dict:
    '''
    Loads a TOML file to a dictionary.

    :param f: The file to read from.

    :type f: str

    :return: Dictionary of TOML file.

    :rtype: dict

    :raises FileNotFoundError: If the file cannot be found at the given location.
    '''

    # Check if the file exists
    if not os.path.exists(f):
        # [;] Could not find the file: failure
        raise FileNotFoundError("File was not found at the given location.")

    # Read the file and return as a dictionary
    with open(f, 'r', encoding="utf-8") as file:
        return tmlk.parse(file.read())

# Modify a specific key
def modify_nested(keys: list[Any], new: Any, f: str) -> bool:
    '''
    Can update a key at any depth in TOML.

    :param keys: A *list* of keys leading to the target key.
    :param new: The value to update the targeted key/value with.
    :param f: The file to read and write to.

    :type keys: list
    :type new: arr | int | str | float | dict
    :type f: str

    :return: Returns True or False

    :rtype: bool

    :raises FileNotFoundError: If the file cannot be found at the given location.
    :raises Exception: Such as KeyError, TypeError, or FileNotFoundError when writing the change.

    > **Warning:** This will modify a key in the targeted file.
    '''

    # 1. CHECK IF FILE EXISTS
    if os.path.exists(f):
        with open(f, 'r', encoding="utf-8") as file:
            data = tmlk.parse(file.read())
    else:
        # [;] Return error
        raise FileNotFoundError("File was not found at the given location.")

    # 2. LOCATE AND UPDATE DATA POINT
    current_depth = data
    try:
        # Loop through key list and navigate through TOML file
        for key in keys[:-1]:
            current_depth = current_depth[key]

        # Once the target key has been found, add it to a variable
        final = keys[-1]
        # Set the value of the target key
        current_depth[final] = new
    except(KeyError, TypeError, FileNotFoundError) as e:
        # [;] Return False if failure
        return False

    # 3. REWRITE TOML FILE WITH NEW DATA USING TEMP FILE
    # [^] Create and dump to temp file
    # [*] Temp file prevents data loss
    temp_name = f + '.tmp'
    with open(temp_name, 'w', encoding="utf-8") as file:
        file.write(tmlk.dumps(data))
    # [^] Replace old main file with new temp file
    os.replace(temp_name, f)

    # [!] 4. RETURN SUCCESSFUL MODIFICATION
    return True

