"""
File name: tcl_manager
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: subprocess, time
Descriptions: Vivado subprocess
"""

from ..pyvado_process import PyvadoProcess
from ..pyvado_session import PyvadoSession
from .pyvado_manager import PyvadoManager

class TCLManager(PyvadoManager):
  """
  run direct TCL command

  Methods
  -------
  run(cmd : str | list[str], blocking : bool = True)
    run TCL command
  
  """

  def __init__(self, 
               vivado_process : PyvadoProcess, 
               pyvado_session : PyvadoSession
              ):
    
    super().__init__(
      vivado_process = vivado_process, 
      pyvado_session = pyvado_session)
    
  def run(self, cmd : str | list[str], blocking : bool = True):
    """
    run TCL command

    Attributes
    ----------
    cmd : str | list[str]
      TCL or list of TCL commands
    blocking : bool = True
      block function until all command are executed
    """

    self._vivado_process.send(
      cmd = cmd,
      blocking = blocking
    )

  def read(self) -> str:
    """
    read vivado output

    Returns
    -------
    str:
      vivado output line
    """

    return self._vivado_process.read()