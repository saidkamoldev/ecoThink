from ursina import Ursina, color
from ursina.prefabs.first_person_controller import FirstPersonController
from resources import Resurslar
from ui import UI
import random
import sys
import traceback

# buildings3d.py dan funksiyalarni import qilish
from buildings3d import create_house, create_factory, create_tree, create_solar_panel, create_water_tower

def main():
    try:
        # O'yin dasturini yaratish
        app = Ursina(fullscreen=False, development_mode=False)
        
        # O'yin modulini import qilish
        import game3d
        
        # O'yinni boshlash
        game3d.start_game()
        
        print("[LOG] Dastur boshlandi. Kursor ko'rinadi.")
        print("[LOG] O'yin boshqaruvi:")
        print("  - WASD: Harakatlanish")
        print("  - SPACE: Sakrash") 
        print("  - ESC: Kursor/Menyu")
        print("  - O'ng tugma: Bino qurish")
        print("  - Chap tugma: Qurilishni bekor qilish")
        
        # O'yinni ishga tushirish
        app.run()
        
    except Exception as e:
        print(f"[ERROR] O'yin ishga tushirishda xatolik: {e}")
        print("[ERROR] Xatolik tafsilotlari:")
        traceback.print_exc()
        input("Dasturni yopish uchun Enter tugmasini bosing...")
        sys.exit(1)

if __name__ == "__main__":
    main() 