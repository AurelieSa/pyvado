"""
File name: pyvado_manager
Author: aureliesa
Version: 1.1.0
License: GPL-3.0-or-later
Dependencies: pyvado_session
Descriptions: Basic pyvado manager
"""

from ..pyvado_session import PyvadoSession

class PyvadoManager():
  """
  Basic Pyvado Manager
  """

  def __init__(self,
               pyvado_session : PyvadoSession
              ):
    self._pyvado_session = pyvado_session