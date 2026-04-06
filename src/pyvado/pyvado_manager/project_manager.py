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
  open_project()
    open vivado project
  close_project()
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

  def open_project(self):
    """
    Open vivado project
    """
    
    self._vivado_process.send(
      cmd = f"open_project {self._pyvado_session.get_project_path()}",
      blocking = True
    )
    self._pyvado_session.open_project()

  def close_project(self):
    """
    close vivado project
    """
    
    self._vivado_process.send(
      cmd = "close_project",
      blocking = True
    )
    self._pyvado_session.close_project()

  def set_toplevel(self, module_name : str):
    """
    setup toplevel
    """

    if not self._pyvado_session.is_project_open():
      raise PyvadoError("project must be open")
    
    self._vivado_process.send([
      f"set_property top {module_name} [current_fileset]",
      "update_compile_order -fileset sources_1",
    ])