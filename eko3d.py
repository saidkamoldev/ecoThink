# Bu fayl endi bo'sh. Kodlar modullarga ajratildi. 

def update_text(self):
    return dedent(f'''
        Pul: {self.pul}$
        Energiya: {self.energiya}%
        Suv: {self.suv}%
        Daraxtlar: {self.daraxtlar}
        Ifloslanish: {self.ifloslanish}%
    ''').strip() 