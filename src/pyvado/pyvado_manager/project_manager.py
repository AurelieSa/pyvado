"""
File name: prject_manager
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: pyvado_process, pyvado_session, pyvado_manager, pyvado_error
Descriptions: Pyvado project manager
"""

from ..pyvado_session import PyvadoSession
from ..pyvado_process import PyvadoProcess
from .pyvado_manager import PyvadoManager
from ..pyvado_error import PyvadoError

class ProjectManager(PyvadoManager):
  """
  Vivado project manager

  Attributes
  ----------

  Methods
  -------
  open()
    open vivado project
  close()
    close vivado project
  set_toplevel()
    set top level module
  """

  def __init__(self,
               vivado_process : PyvadoProcess,
               pyvado_session : PyvadoSession
              ):
    """
    ProjectManager constructor

    Parameters
    ----------
    vivado_process : PyvadoProcess
      vivado consol process
    pyvado_session : PyvadoSession
      pyvado session
    """
    
    super().__init__(
      vivado_process = vivado_process,
      pyvado_session = pyvado_session
    )

  def open(self):
    """
    Open vivado project
    """
    
    self._vivado_process.send(
      cmd = f"open_project {self._pyvado_session.project_path}",
      blocking = True
    )
    self._pyvado_session.project.open()

  def close(self):
    """
    close vivado project
    """
    
    self._vivado_process.send(
      cmd = "close_project",
      blocking = True
    )
    self._pyvado_session.project.close()

  