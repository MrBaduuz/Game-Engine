import sys
engine_path = sys.path[0].replace("Examples", "")
sys.path.append(engine_path)
import Engine as eng
eng.createGame("Drums", 600, 600, 60)





eng.run()