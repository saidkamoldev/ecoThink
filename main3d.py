from ursina import Ursina

app = Ursina()

import game3d

game3d.start_game()

print("[LOG] Dastur boshlandi. Kursor ko'rinadi.")
app.run() 