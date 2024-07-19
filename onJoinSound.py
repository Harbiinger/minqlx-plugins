import minqlx
import minqlx.database

_onjoinsound_key = "minqlx:players:{}:onjoin_sound"

class OnJoinSound(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded, priority=minqlx.PRI_LOWEST)
        self.add_command(("onjoinsound", "ojs"), self.cmd_onjoinsound, usage="<message>", client_cmd_perm=0)

    def cmd_onjoinsound(self, player, msg, channel):
        onjoinsound_key = _onjoinsound_key.format(player.steam_id)
        if len(msg) < 2:
            return minqlx.RET_USAGE
        else:
            del self.db[onjoinsound_key]
            player.tell("Your onjoin sound has been removed.")
            return minqlx.RET_STOP_ALL
    sound = str(" ".join(msg[1:]))

    self.db[onjoinsound_key] = sound
    player.tell("That sound has been saved. To make me forget about it, a simple ^4{}onjoin^7 will do it.".format(self.get_cvar("qlx_commandPrefix")))
    return minqlx.RET_STOP_ALL

    def handle_player_loaded(self, player):
        onjoinsound_key = _onjoinsound_key.format(player.steam_id)
        if onjoin_key in self.db:
            onjoin_sound = self.db[onjoinsound_key]
            for p in self.players():
                if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                    super().play_sound(onjoin_sound)
