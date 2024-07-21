import minqlx 
import re

_whitelist_key = "minqlx:players:{}:whitelisted"

class whitelist(minqlx.Plugin):
    def __init__(self):
        self.add_command(("whitelistadd", "wladd"), self.cmd_whitelistadd, usage="<steam_id>", client_cmd_perm=5)
        self.add_command(("whitelistremove", "wlrem"), self.cmd_whitelistremove, usage="<steam_id>", client_cmd_perm=5)
        self.add_hook("player_connect", self.handle_player_connect)
        
        admin = self.get_cvar("qlx_owner", str)
        self.cmd_whitelistadd(None, [None, admin], None)

    def cmd_whitelistadd(self, player, msg, channel):
        if not re.match(r'^\d+$', msg[1]):
            player.tell("Incorrect steam_id.")
            return minqlx.RET_STOP_ALL

        whitelist_key = _whitelist_key.format(msg[1])

        if whitelist_key not in self.db:
            self.db[whitelist_key] = True
            if player != None:
                player.tell("steam_id added to the whitelist.")

        elif player != None:
            player.tell("This steam_id is already whitelisted.")

    def cmd_whitelistremove(self, player, msg, channel):
        if not re.match(r'^\d+$', msg[1]):
            player.tell("Incorrect steam_id.")
            return minqlx.RET_STOP_ALL

        whitelist_key = _whitelist_key.format(msg[1])

        if whitelist_key in self.db:
            del self.db[whitelist_key]
            player.tell("steam_id removed from whitelist.")

        else:
            player.tell("This steam_id is not whitelisted.")

    def handle_player_connect(self, player):
        whitelist_key = _whitelist_key.format(player.steam_id)
        if whitelist_key not in self.db:
            player.kick("You are not whitelisted on this server.")
