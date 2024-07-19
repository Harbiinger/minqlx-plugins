import minqlx
import re

_onjoinsound_key = "minqlx:players:{}:onjoin_sound"

class onJoinSound(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded, priority=minqlx.PRI_LOWEST)
        self.add_hook("death", self.handle_death)
        self.add_command(("onjoinsound", "ojs"), self.cmd_onjoinsound, usage="<sound path> (ex: !ojs sound/funnysounds/imperial.ogg)", client_cmd_perm=0)
        self.add_command(("forcejoinsound", "fjs"), self.cmd_forcejoinsound, usage="<player steam_id> <sound path>", client_cmd_perm=4)

    def cmd_onjoinsound(self, player, msg, channel):
        onjoinsound_key = _onjoinsound_key.format(player.steam_id)
        if len(msg) < 2:
            if onjoinsound_key not in self.db:
                return minqlx.RET_USAGE
            else:
                del self.db[onjoinsound_key]
                player.tell("Your onjoin sound has been removed.")
                return minqlx.RET_STOP_ALL
        sound = str(" ".join(msg[1:]))

        self.db[onjoinsound_key] = sound
        player.tell("That sound ({}) has been saved. To make me forget about it, a simple ^4{}onjoinsound^7 will do it.".format(sound, self.get_cvar("qlx_commandPrefix")))
        return minqlx.RET_STOP_ALL

    def cmd_forcejoinsound(self, player, msg, channel):
        if not re.match(r'^\d+$', msg[1]):
            player.tell("Incorrect steam_id format.")
            return minqlx.RET_STOP_ALL 
        onjoinsound_key = _onjoinsound_key.format(msg[1])
        if len(msg) < 3:
            if onjoinsound_key not in self.db:
                return minqlx.RET_USAGE
            else:
                del self.db[onjoinsound_key]
                player.tell("The onjoin sound for {} has been removed.".format(msg[1]))
                return minqlx.RET_STOP_ALL
        sound = str(" ".join(msg[2]))
        self.db[onjoinsound_key] = sound
        player.tell("That sound ({}) has been saved. To make me forget about it, a simple ^4{}forcejoinsound {}^7 will do it.".format(sound, self.get_cvar("qlx_commandPrefix", msg[1])))

    def handle_player_loaded(self, player):
        onjoinsound_key = _onjoinsound_key.format(player.steam_id)
        if onjoinsound_key in self.db:
            for p in self.players():
                if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                    super().play_sound(self.db[onjoinsound_key])

    def handle_death(self, victim, killer, data):
        if victim.steam_id == killer.steam_id or killer.steam_id == "":
            for p in self.players():
                if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                    super().play_sound("sound/funnysounds/DumbWays.ogg")
