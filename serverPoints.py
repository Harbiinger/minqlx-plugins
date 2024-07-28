import minqlx

_serverPoints_key = "minqlx:player:{}:serverPoints"

class serverPoints(minqlx.Plugin):
    def __init__(self):
        self.add_hook("death", self.handle_death)
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("kill", self.handle_kill)
        self.add_hook("server_command", self.handle_server_command)
        self.add_command("points", self.cmd_points, client_cmd_perm=0)

    def handle_player_loaded(self, player):
        serverPoints_key = _serverPoints_key.format(player.steam_id)
        if serverPoints_key not in self.db:
            self.db[serverPoints_key] = 0

        player.tell("Server Points enabled: kill -> 1pt; win -> 10pts; suicide -> -5pts. ^6!points^7 to see your points")

    def handle_kill(self, victim, killer, data):
        if victim.steam_id != killer.steam_id and self.game.state == 'in_progress':
            serverPoints_key = _serverPoints_key.format(killer.steam_id)
            pts = int(self.db[serverPoints_key])
            self.db[serverPoints_key] = pts + 1
            killer.tell("^2(+1 pt | kill)")

    def handle_death(self, victim, killer, data):
        if  self.game.state == 'in_progress' and (killer is None or victim.steam_id == killer.steam_id):
            serverPoints_key = _serverPoints_key.format(victim.steam_id)
            pts = int(self.db[serverPoints_key])
            if pts >= 5:
                self.db[serverPoints_key] = pts - 5
                victim.tell("^2(-5 pts | suicide)")

    def handle_game_end(self, data):
        max_frags = 0
        winners = []
        for p in self.players():
            if p.team == 'free' and p.score > max_frags:
                max_frags = p.score
                if len(winners) > 0:
                    winners[0] = p
                else:
                    winners.append(p)
            elif p.team == 'red' and self.game.red_score > self.game.blue_score:
                winners.append(p)
            elif p.team == 'blue' and self.game.blue_score > self.game.red_score:
                winners.append(p)
        for p in winners:
            serverPoints_key = _serverPoints_key.format(p.steam_id)
            pts = int(self.db[serverPoints_key])
            self.db[serverPoints_key] = pts + 10
            p.tell("^2(+10 pts | win)")


    def handle_server_command(self, player, cmd):
        args = cmd.split()
        if args[0] == 'chat':
            serverPoints_key = _serverPoints_key.format(player.steam_id)
            cmd = cmd.replace(player.name, "[{}] {}".format(self.db[serverPoints_key], player.name))
            return cmd

    def cmd_points(self, player, cmd, channel):
        serverPoints_key = _serverPoints_key.format(player.steam_id)
        player.tell("You have ^2{} ^7points.".format(self.db[serverPoints_key]))
