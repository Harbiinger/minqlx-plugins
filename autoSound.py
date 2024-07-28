import minqlx

DEATH_SOUND = "sound/funnysounds/DumbWays.ogg"

class autoSound(minqlx.Plugin):
    def __init__(self):
        self.add_hook("death", self.handle_death)

    def handle_death(self, victim, killer, data):
        if killer is None or victim.steam_id == killer.steam_id:
            for p in self.players():
                if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                    super().play_sound(DEATH_SOUND)
