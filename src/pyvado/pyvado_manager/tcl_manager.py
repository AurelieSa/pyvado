"""
File name: tcl_manager
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Dependencies: pyvado_session, pyvado_manager
Descriptions: Pyvado TCL command manager
"""

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
               pyvado_session : PyvadoSession
              ):
    
    super().__init__( 
      pyvado_session = pyvado_session
    )
    
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

    self._pyvado_session.process.send(
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

    return self._pyvado_session.process.read()