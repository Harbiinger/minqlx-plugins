import minqlx

_onjoinsound_key = "minqlx:players:{}:onjoin_sound"

class onJoinSound(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded, priority=minqlx.PRI_LOWEST)
        self.add_command(("onjoinsound", "ojs"), self.cmd_onjoinsound, usage="<sound path> (ex: !ojs sound/funnysounds/imperial.ogg)", client_cmd_perm=0)

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

    @minqlx.delay(2)
    def handle_player_loaded(self, player):
        onjoinsound_key = _onjoinsound_key.format(player.steam_id)
        if onjoinsound_key in self.db:
            player.tell("{}".format(self.db[onjoinsound_key]))
            onjoin_sound = self.db[onjoinsound_key]
            player.tell("[onJoinSound] playing sound:", onjoin_sound)
            for p in self.players():
                if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                    super().play_sound(onjoin_sound)
        else:
            player.tell("Reminder! you can use ^4{}onjoinsound^7 to choose a sound that will be played when you join the server.".format(self.get_cvar("qlx_commandPrefix")))
