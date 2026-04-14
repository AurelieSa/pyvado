"""
File name: pyvado_manager
Author: aureliesa
Version: 1.0.0
License: GPL-3.0-or-later
Dependencies: pyvado_process, pyvado_session
Descriptions: Basic pyvado manager
"""

from ..pyvado_process import PyvadoProcess
from ..pyvado_session import PyvadoSession

class PyvadoManager():
  """
  Basic Pyvado Manager
  """

  def __init__(self,
               vivado_process : PyvadoProcess,
               pyvado_session : PyvadoSession
              ):
    self._vivado_process = vivado_process
    self._pyvado_session = pyvado_session