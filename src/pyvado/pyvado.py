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
from .pyvado_process import PyvadoProcess
from .pyvado_error import PyvadoError

class Pyvado:
  """
  Python vivado API wrapper

  Methods
  -------
  run_command(cmd : str | list[str], blocking : bool = True)
    run vivado command line(s)
  open_project()
    open vivado project
  close_project()
    close vivado project
  project_open() -> bool:
    return flag if vivado project is open

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


    self.__vivado_process = PyvadoProcess(
      vivado_command = vivado_command,
      timeout = process_timeout
    )

    if project_path == "" or project_path is None:
      raise ValueError("no project path") 
    
    if len(project_name) < 4 :
      raise ValueError("invalid project name")

    if project_name[-4:] != ".xpr":
      raise ValueError("project name must finish with xpr extension")
    

    self.__project_name = project_name
    self.__projec_path = os.path.abspath(project_path)
    self.__is_project_open = False

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
      cmd = f"open_project {os.path.join(self.__projec_path, self.__project_name)}",
      blocking = True
    )
    self.__is_project_open = True

  def close_project(self):
    """
    close vivado project
    """
    
    self.run_command(
      cmd = "close_project",
      blocking = True
    )
    self.__is_project_open = False

  def project_open(self) -> bool:
    """
    return flag if vivado project is open
    """
    
    return self.__is_project_open 

  def __enter__(self):
    self.open_project()
    return self
  
  def __exit__(self, exc_type, exc, tb):

    if self.project_open():
      self.close_project()
    self.__vivado_process.close()

  def add_file(self, file_path : str, synth_only : bool = False, simu_only : bool = False):
    """
    Add file to vivado project

    Parameters
    ----------
    file_path : str
      path of file to add
    synth_only : bool = False
      added file will be available only for synthesis
    simu_only : bool = False
      added file will be available only for simulation
    """

    if not self.project_open():
      raise PyvadoError("project must be open to add file")

    if synth_only and simu_only:
      raise ValueError("a file must be at least in simulation or synthesis")
    
    file_path = os.path.abspath(file_path)

    cmd = [
      f"add_files -norecurse \"{file_path}\"",
      "update_compile_order"
    ]

    if synth_only:
      cmd.append(f"set_property used_in_simulation false [get_files {file_path}]")
    elif simu_only:
      cmd.append(f"set_property used_in_synthesis false [get_files {file_path}]")

    self.run_command(
      cmd = cmd,
      blocking = True
    )
