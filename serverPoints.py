import minqlx

_serverPoints_key = "minqlx:player:{}:serverPoints"

class serverPoints(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("kill", self.handle_kill)
        self.add_hook("death", self.handle_death)
        self.add_hook("server_command", self.handle_server_command)

    def handle_player_loaded(self, player):
        serverPoints_key = _serverPoints_key.format(killer.steam_id)
        if serverPoints_key not in self.db:
            self.db[serverPoints_key] = 0

        player.tell("You have ^2{} ^7points.".format(self.db[serverPoints_key]))

    def handle_kill(self, victim, killer, data):
        if victim.steam_id != killer.steam_id:
            serverPoints_key = _serverPoints_key.format(killer.steam_id)
            pts = int(self.db[serverPoints_key])
            self.db[serverPoints_key] = pts + 1
            killer.tell("^2(+1 pt | kill)")

    def handle_death(self, victim, killer, data):
        if killer is None or killer.steam_id == victim.steam_id:
            serverPoints_key = _serverPoints_key.format(victim.steam_id)
            pts = int(self.db[serverPoints_key])
            if pts >= 5:
                self.db[serverPoints_key] = pts - 5
                killer.tell("^2(-5 pts | suicide)")

    def handle_game_end(self, data):
        pass #TODO 

    def handle_server_command(self, player, cmd):
        args = cmd.split()
        if args[0] == 'chat':
            serverPoints_key = _serverPoints_key.format(player.steam_id)
            cmd = cmd.replace(player.name, "[{}] {}".format(self.db[serverPoints_key], player.name))
            return cmd
