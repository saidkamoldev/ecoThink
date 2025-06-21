from textwrap import dedent

class Resurslar:
    def __init__(self):
        self.pul = 5000
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
        
        # Ekologiya balansini hisoblash - kuchaytirilgan formula
        self.ekologiya_balansi = max(0, 100 - self.ifloslanish * 3 + self.daraxtlar * 3)  # 5, 2 → 3, 3
        
        print(f"[DEBUG] Qurishdan keyin: Pul={self.pul}, Energiya={self.energiya}, Suv={self.suv}, Daraxtlar={self.daraxtlar}, Ifloslanish={self.ifloslanish}, Ekologiya={self.ekologiya_balansi}")
        
        # Ogohlantirishlarni tekshirish
        self.ogohlantirishlarni_tekshirish(qurilma, eski_balans)
        
        # Manfiy resurslarni cheklash
        self.resurslarni_cheklash()
        
    def ogohlantirishlarni_tekshirish(self, qurilma, eski_balans):
        """Ogohlantirishlarni tekshirish va qo'shish"""
        # Pul tugab qolsa
        if self.pul < 0:
            self.ogohlantirishlar.append("⚠️ Pul tugab qoldi! Iqtisodiy inqiroz!")
            
        # Energiya tugab qolsa
        if self.energiya < 0:
            self.ogohlantirishlar.append("⚡ Energiya yetishmayapti! Elektr uzilishi!")
            
        # Suv tugab qolsa
        if self.suv < 0:
            self.ogohlantirishlar.append("💧 Suv yetishmayapti! Suv tanqisligi!")
            
        # Ifloslanish juda ko'p bo'lsa
        if self.ifloslanish > 15:  # 20 → 15 (tezroq ogohlantirish)
            self.ogohlantirishlar.append("🌫️ Ifloslanish juda ko'p! Atrof-muhit xavfi!")
            
        # Ekologiya balansi past bo'lsa
        if self.ekologiya_balansi < 40:  # 30 → 40 (tezroq ogohlantirish)
            self.ogohlantirishlar.append("🌍 Ekologiya balansi past! Tabiat xavfi!")
            
        # Ekologiya balansi yaxshilangsa
        if self.ekologiya_balansi > eski_balans and self.ekologiya_balansi > 70:
            self.ogohlantirishlar.append("✅ Ekologiya balansi yaxshilandi! Tabiat saqlanmoqda!")
            
        # Daraxtlar ko'payganda
        if self.daraxtlar > 15:  # 20 → 15 (tezroq xabar)
            self.ogohlantirishlar.append("🌳 Daraxtlar ko'paydi! Yashil shahar!")
            
        # Zavod qurilganda maxsus ogohlantirish
        if qurilma['nom'] == 'Zavod':
            self.ogohlantirishlar.append("🏭 Zavod qurildi! Ifloslanish ko'paydi!")
            
        # Daraxt qurilganda maxsus xabar
        if qurilma['nom'] == 'Daraxt':
            self.ogohlantirishlar.append("🌳 Daraxt qurildi! Ekologiya yaxshilandi!")
            
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