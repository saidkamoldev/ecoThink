from textwrap import dedent

class Resurslar:
    def __init__(self):
        self.pul = 8000
        self.energiya = 100
        self.suv = 100
        self.daraxtlar = 10
        self.ifloslanish = 0
        self.ekologiya_balansi = 100
        self.ogohlantirishlar = []
        
    def resurs_qoshish(self, qurilma):
        """Qurilma qo'shilganda resurslarni yangilash"""
        eski_balans = self.ekologiya_balansi
        
        print(f"[DEBUG] Qurishdan oldin: Pul={self.pul}, Energiya={self.energiya}, Suv={self.suv}, Daraxtlar={self.daraxtlar}, Ifloslanish={self.ifloslanish}")
        print(f"[DEBUG] Qurilma: {qurilma['nom']}, Narx={qurilma['narx']}, Energiya={qurilma['energiya']}, Suv={qurilma['suv']}, Daraxtlar={qurilma['daraxtlar']}, Ifloslanish={qurilma['ifloslanish']}")
        
        # Resurslarni yangilash
        self.pul -= qurilma['narx']
        self.energiya += qurilma['energiya']
        self.suv += qurilma['suv']
        self.daraxtlar += qurilma['daraxtlar']
        self.ifloslanish += qurilma['ifloslanish']
        
        # Ekologiya balansini hisoblash - 100% dan o'tmasin
        self.ekologiya_balansi = max(0, min(100, 100 - self.ifloslanish * 4 + self.daraxtlar * 6))
        
        print(f"[DEBUG] Qurishdan keyin: Pul={self.pul}, Energiya={self.energiya}, Suv={self.suv}, Daraxtlar={self.daraxtlar}, Ifloslanish={self.ifloslanish}, Ekologiya={self.ekologiya_balansi}")
        
        # Faqat bitta xabar berish
        self.bitta_xabar_berish(qurilma, eski_balans)
        
        # Manfiy resurslarni cheklash
        self.resurslarni_cheklash()
        
    def bitta_xabar_berish(self, qurilma, eski_balans):
        """Faqat bitta xabar berish - ikkita emas"""
        nom = qurilma['nom'].lower()
        print(f"[DEBUG] Xabar berish: {qurilma['nom']} (lower: {nom})")
        
        # Faqat asosiy xabar - boshqa xabarlar yo'q
        if nom == 'zavod':
            xabar = f"🏭 Zavod qurildi! Ifloslanish +{qurilma['ifloslanish']}"
            self.ogohlantirishlar.insert(0, xabar)
            print(f"[DEBUG] Zavod xabari qo'shildi: {xabar}")
        elif nom == 'daraxt':
            xabar = f"🌳 Daraxt qurildi! Ekologiya yaxshilandi"
            self.ogohlantirishlar.insert(0, xabar)
            print(f"[DEBUG] Daraxt xabari qo'shildi: {xabar}")
        elif nom == 'quyosh paneli':
            xabar = f"☀️ Quyosh paneli qurildi! Energiya +{qurilma['energiya']}"
            self.ogohlantirishlar.insert(0, xabar)
            print(f"[DEBUG] Quyosh paneli xabari qo'shildi: {xabar}")
        elif nom == 'suv minorasi':
            xabar = f"💧 Suv minorasi qurildi! Suv +{qurilma['suv']}"
            self.ogohlantirishlar.insert(0, xabar)
            print(f"[DEBUG] Suv minorasi xabari qo'shildi: {xabar}")
        elif nom == 'uy':
            xabar = f"🏠 Uy qurildi! Energiya {qurilma['energiya']}, Suv {qurilma['suv']}"
            self.ogohlantirishlar.insert(0, xabar)
            print(f"[DEBUG] Uy xabari qo'shildi: {xabar}")
        print(f"[DEBUG] Jami ogohlantirishlar soni: {len(self.ogohlantirishlar)}")
        
        # Faqat juda muhim ogohlantirishlar
        if self.pul < 0:
            self.ogohlantirishlar.append("⚠️ Pul tugab qoldi!")
        if self.energiya < 0:
            self.ogohlantirishlar.append("⚡ Energiya yetishmayapti!")
        if self.suv < 0:
            self.ogohlantirishlar.append("💧 Suv yetishmayapti!")
        if self.ekologiya_balansi < 20:
            self.ogohlantirishlar.append("🌍 Ekologiya balansi past!")
        
    def resurslarni_cheklash(self):
        """Manfiy resurslarni 0 ga cheklash"""
        self.energiya = max(0, self.energiya)
        self.suv = max(0, self.suv)
        self.daraxtlar = max(0, self.daraxtlar)
        self.ifloslanish = max(0, self.ifloslanish)
        
    def oxirgi_ogohlantirishni_olish(self):
        """Oxirgi ogohlantirishni olish va o'chirish"""
        if self.ogohlantirishlar:
            return self.ogohlantirishlar.pop(0)
        return None
        
    def update_text(self):
        return dedent(f'''
            💰 Pul: {self.pul:,}$
            ⚡ Energiya: {self.energiya} MW
            💧 Suv: {self.suv} L
            🌳 Daraxtlar: {self.daraxtlar}
            🌫️ Ifloslanish: {self.ifloslanish}
            🌍 Ekologiya: {self.ekologiya_balansi:.0f}%
        ''').strip()