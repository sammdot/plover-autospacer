from threading import Thread

from plover.steno import Stroke
from plover.translation import Translation

SYSTEM_NAMES = [
  "Japanese",
  "Chinese",
  "Cantonese",
  "Thai",
]

class AutoSpacer(Thread):

  def __init__(self, engine):
    super().__init__()
    self.engine = engine
    self.engine.hook_connect("config_changed", self._on_config_changed)

  def start(self):
    self._on_config_changed(None)
    super().start()

  def stop(self):
    pass

  @staticmethod
  def needs_zero_space(system):
    return any(name in system for name in SYSTEM_NAMES)

  def _on_config_changed(self, _):
    tl = Translation([Stroke([])],
      "{mode:set_space:}"
      if AutoSpacer.needs_zero_space(self.engine.config["system_name"]) else
      "{mode:reset_space}")
    self.engine._translator.translate_translation(tl)
