"""The enhanced smoke also covers opponent intent, forms and resource decisions."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('enhanced_combat_ui_smoke.py')),run_name='__main__')
