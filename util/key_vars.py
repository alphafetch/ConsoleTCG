from pathlib import Path

class KeyVars():
    user_data_toml = str(Path.home() / 'ConsoleTCG' / 'userdata.toml')
    user_data_dir = str(Path.home() / 'ConsoleTCG')