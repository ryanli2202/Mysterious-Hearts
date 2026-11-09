import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import game_core as c

print('Model:', c.check_model(), flush=True)
result = c.generate(c.fresh('rei'), 'Hi Emily. How has the flower shop been today?')
print('Validated live scene:', result, flush=True)
