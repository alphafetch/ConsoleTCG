from pathlib import Path

class KeyVars():
    user_data_toml = str(Path.home() / 'ConsoleTCG' / 'userdata.toml')
    user_decks_toml = str(Path.home() / 'ConsoleTCG' / 'userdecks.toml')

    cards_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'cards.toml')
    profiles_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'profiles.toml')
    career_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'career.toml')