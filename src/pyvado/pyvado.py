"""
File name: pyvado
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: os, vivadoProcess
Descriptions: Vivado Python API wrapper
"""

import os
from .vivadoProcess import VivadoProcess

class PyVado:
  """
  Python vivado API wrapper

  Methods
  -------
  run_command(cmd : str | list[str], blocking : bool = True)
    run vivado command line(s)
  open_project()
    open vivado project

  Attributes
  ----------
  project_path : str
    vivado project path
  project_name : str
    vivado project name
  """

  def __init__(self,
               project_name : str,
               project_path : str,
               vivado_command : str = "vivado",
               process_timeout : int = 600
              ):
    """
    PyVado constructor

    Parameters
    ----------
    project_name : str
      vivado project name. Must be .xpr file
    project_path : str
      vivado project path
    vivado_command : str = "vivado"
      vivado command line
    process_timeout : int = 600
      vivado command timeout
    """


    self.__vivado_process = VivadoProcess(
      vivado_command = vivado_command,
      timeout = process_timeout
    )

    self.project_name = project_name
    self.projec_path = project_path
    self.is_project_open = False

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

  def open_project(self):
    """
    Open vivado project
    """
    
    self.run_command(
      cmd = f"open_project {self.projec_path}/{self.project_name}",
      blocking = True
    )
    self.is_project_open = True

  def __enter__(self):
    self.open_project()
    return self
  
  def __exit__(self, exc_type, exc, tb):

    if self.is_project_open:
      self.run_command(
        cmd = "close_project"
      )
    self.__vivado_process.close()
