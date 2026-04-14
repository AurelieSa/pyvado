"""
File name: project_manager
Author: aureliesa
Version: 1.0.0
License: GPL-3.0-or-later
Dependencies: pyvado_process, pyvado_session, pyvado_manager
Descriptions: Pyvado project manager
"""

from ..pyvado_session import PyvadoSession
from ..pyvado_process import PyvadoProcess
from .pyvado_manager import PyvadoManager

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

    Methods
    -------
    open(project_path : str = "")
      open project
    close()
      close vivado project
    """
    
    super().__init__(
      vivado_process = vivado_process,
      pyvado_session = pyvado_session
    )

  def open(self, project_path : str = ""):
    """
    Open vivado project
    """

    if project_path != "":
      self._pyvado_session.set_project_path(project_path)

    self._vivado_process.send(
      cmd = f"open_project {self._pyvado_session.project_path}",
      blocking = True
    )
    self._pyvado_session.project.open()

  def close(self):
    """
    close vivado project
    """
    
    if self._pyvado_session.project.is_open():
      self._vivado_process.send(
        cmd = "close_project",
        blocking = True
      )
      self._pyvado_session.project.close()

  