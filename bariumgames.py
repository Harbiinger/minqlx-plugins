import minqlx

class bariumgames(minqlx.Plugin):
    def __init__(self):
        self.add_command("info", self.cmd_info, client_cmd_perm=0)

    def cmd_info(self, player, msg, channel):
        player.tell("Commands: \n \
        !info - Displays information about this server's plugins. \n \
        !points - Displays the amount of points you have. (kill -> 1pt; win -> 10pts; suicide -> -5pts) \n \
        ")
