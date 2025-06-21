from textwrap import dedent

class Resurslar:
    def __init__(self):
        self.pul = 5000
        self.energiya = 100
        self.suv = 100
        self.daraxtlar = 10
        self.ifloslanish = 0
    def update_text(self):
        return dedent(f'''
            Pul: {self.pul}$
            Energiya: {self.energiya} MW
            Suv: {self.suv} L
            Daraxtlar: {self.daraxtlar}
            Ifloslanish: {self.ifloslanish}
        ''').strip()