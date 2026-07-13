class CricketMatch:
    def __init__(self):
        self.team_a = None
        self.team_b = None
        self.overs = 20
        self.date = None
        self.pitch_type = "Standard"
        self.is_day_night = False
        self.dl_method = False

    def __str__(self):
        return (f"Match: {self.team_a} vs {self.team_b} on {self.date} | "
                f"Overs: {self.overs} | Pitch: {self.pitch_type} | "
                f"Day/Night: {self.is_day_night} | DLS: {self.dl_method}")

class CricketMatchBuilder:
    def __init__(self):
        self.match = CricketMatch()

    def set_teams(self, team_a, team_b):
        self.match.team_a = team_a
        self.match.team_b = team_b
        return self

    def set_overs(self, overs):
        self.match.overs = overs
        return self

    def set_date(self, date):
        self.match.date = date
        return self

    def set_pitch_type(self, pitch_type):
        self.match.pitch_type = pitch_type
        return self

    def set_is_day_night(self, is_day_night):
        self.match.is_day_night = is_day_night
        return self

    def set_is_dl_method(self, is_dl_method):
        self.match.is_day_night = is_dl_method
        return self

    def build(self) -> CricketMatch:
        return self.match

match_builder = CricketMatchBuilder()

custom_match = (match_builder
                .set_teams("CSK", "MI")
                .set_overs(20)
                .set_is_day_night(True)
                .build())

print(custom_match)