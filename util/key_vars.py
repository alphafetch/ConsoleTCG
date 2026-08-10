from pathlib import Path

class KeyVars():
    user_data_toml = str(Path.home() / 'ConsoleTCG' / 'userdata.toml')
    user_data_dir = str(Path.home() / 'ConsoleTCG')

    cards_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'cards.toml')
    profiles_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'profiles.toml')