from pathlib import Path

class KeyVars():
    # User data
    user_data_toml = str(Path.home() / 'ConsoleTCG' / 'userdata.toml')
    user_decks_toml = str(Path.home() / 'ConsoleTCG' / 'userdecks.toml')

    # Game data
    cards_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'cards.toml')
    profiles_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'profiles.toml')
    career_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'career.toml')
    lvls_toml = str(((Path(__file__).resolve()).parents[1]) / 'src' / 'levels.toml')

    # Damage data
    fire_res = 0.8 # * 0.8 + rand (+-0.1)
    water_res = 0.9 # * 0.9 + rand (+-0.05)
    sun_res = 0.6 # * 0.6 + rand (+-0.3)
    earth_res = 0.75 # * 0.75 + rand (+-0.2)
    nature_res = 0.8 # * 0.8 + rand (+-0.05)

    fire_weak = 1.2 # * 1.2 + rand (+-0.1)
    water_weak = 1.1 # * 1.1 + rand (+-0.05)
    sun_weak = 1.4 # * 1.4 + rand (+-0.3)
    earth_weak = 1.25 # * 1.25 + rand (+-0.2)
    nature_weak = 1.2 # * 1.2 + rand (+-0.05)

    blade_res = 0.7 # * 0.7 + rand (+-0.15)
    blunt_res = 0.9 # * 0.9 + rand (+-0.05)
    hard_res = 0.4 # * 0.4 + rand (+0.4, -0.05)
    wood_res = 0.8 # * 0.8 + rand (+-0.1)

    blade_weak = 1.3 # * 1.3 + rand (+-0.15)
    blunt_weak = 1.1 # * 1.1 + rand (+-0.05)
    hard_weak = 1.6 # * 1.6 + rand (-0.4, +0.05)
    wood_weak = 1.2 # * 1.2 + rand (+-0.1)