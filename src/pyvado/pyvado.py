"""
File name: pyvado
Author: aureliesa
Version: 0.2.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: pyvado_process, pyvado_session, pyvado_manager
Descriptions: Vivado Python API wrapper
"""

from .pyvado_process import PyvadoProcess
from .pyvado_session import PyvadoSession
from .pyvado_manager import *

class Pyvado:
  """
  Python vivado API wrapper

  Methods
  -------
  run_command(cmd : str | list[str], blocking : bool = True)
    run vivado command line(s)
  read_output() -> str:
    read vivado process output
  
  
  Attributes
  ----------
  session : PyvadoSession
    pyvado session data structure
  project_manager : ProjectManager
    pyvado project manager
  flow_manager : FlowManager
    pyvado synthesis flow manager
  """

  def __init__(self,
               project_path : str,
               vivado_command : str = "vivado",
               process_timeout : int = 600
              ):
    """
    PyVado constructor

    Parameters
    ----------
    project_path : str
      vivado project path
    vivado_command : str = "vivado"
      vivado command line
    process_timeout : int = 600
      vivado command timeout
    """


    self.__vivado_process = PyvadoProcess(
      vivado_command = vivado_command,
      timeout = process_timeout
    )

    self.session = PyvadoSession(
      project_path = project_path
    )

    self.project_manager = ProjectManager(
      vivado_process = self.__vivado_process,
      pyvado_session = self.session
    )

    self.flow_manager = FlowManager(
      vivado_process = self.__vivado_process,
      pyvado_session = self.session
    )

  def run_command(self, cmd : str | list[str], blocking : bool = True):
    """
    run vivado command line(s)

    Parameters
    ----------
    cmd : str | list[str]
      command line(s)
    blocking : bool = True
      wait for the end of command line execution if True
    """
    self.__vivado_process.send(
      cmd = cmd,
      blocking = blocking
    )

  def read_output(self) -> str:
    """
    read vivado process output
    """
    
    return self.__vivado_process.read()

  def __enter__(self):
    self.project_manager.open_project()
    return self
  
  def __exit__(self, exc_type, exc, tb):

    if self.session.is_project_open():
      self.project_manager.close_project()
    self.__vivado_process.close()

  