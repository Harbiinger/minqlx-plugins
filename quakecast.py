import minqlx
from minqlx.database import Redis

class quakecast(minqlx.Plugin):
    db = redis

    def _init__(self):
        super.__init__()
        self.add_command("podcast", self.handle_podcast)

    def handle_podcast(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        if msg[]

        
    def play_sound(self, path):
        if not self.last_sound:
            pass
        elif time.time() - self.last_sound < self.get_cvar("qlx_funSoundDelay", int):
            return

        self.last_sound = time.time()
        for p in self.players():
            if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                super().play_sound(path, p)
