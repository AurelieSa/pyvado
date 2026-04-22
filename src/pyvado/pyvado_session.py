"""
File name: pyvado_session
Author: aureliesa
Version: 1.2.0
License: GPL-3.0-or-later
Dependencies: pathlib, pyvado_error
Descriptions: Vivado Python API wrapper
"""

from pathlib import Path
from .pyvado_error import PyvadoError
from .pyvado_process import PyvadoProcess

class OpenState():
  """
  Session open Manager
  """

  def __init__(self):
    self.__open = False

  def is_open(self) -> bool:
    """
    return if entity is open

    Returns
    -------
      bool
    """
    return self.__open
  
  def open(self):
    """
    Open entity
    """

    self.__open = True

  def close(self):
    """
    Close entity
    """
    
    self.__open = False

class PyvadoSession():
  """
  Pyvado project session to store global project informations

  Attributes
  ----------
  project : EntityOpenManager
    project open manager
  hardware : EntityOpenManager
    hardware open manager
  target : EntityOpenManager
    hardware target open manager
  hw_server : EntityOpenManager
    hardware server open manager
  simulator : EntityOpenManager
    simulator open manager
  saif : EntityOpenManager
    saif open manager
  session : PyvadoProcess
    vivado process

  Methods
  -------
  get_project_path() ->  Path
    return project path
  get_project_dir() -> Path
    return project directory
  get_project_name() -> Path
    return project name (without .xpr)
  get_part(filter : str = "") -> list[str]
    get hardware installed parts
  get_boards(filter : str = "") -> list[str]
    get installed boards
  """

  def __init__(self,
               project_path : str = "",
               vivado_command : str = "vivado",
               process_timeout : int = 600
              ):
    """
    Class Constructor

    Parameters
    ----------
    project_path : str = ""
      vivado project path. Can be set after initialisation
    """
    if project_path == "" or project_path is None:
      self.__project_path = None
    else:
      self.set_project_path(project_path)

    self.__project = OpenState()

    self.__hardware = OpenState()

    self.__target = OpenState()

    self.__hw_server = OpenState()

    self.__simulator = OpenState()

    self.__saif = OpenState()

    self.__vivado_process = PyvadoProcess(
      vivado_command = vivado_command,
      timeout = process_timeout
    )

  @property
  def process(self) -> PyvadoProcess:
    return self.__vivado_process

  def set_project_path(self, path : str):
    
    path = Path(path).resolve()

    if path.suffix != ".xpr":
      raise ValueError("project name must finish with xpr extension")
    
    self.__project_path = Path(path).resolve()

  @property
  def project(self) -> OpenState:
    return self.__project
  
  @property
  def hardware(self) -> OpenState:
    return self.__hardware
  
  @property
  def target(self) -> OpenState:
    return self.__target
  
  @property
  def hw_server(self) -> OpenState:
    return self.__hw_server
  
  @property
  def simulator(self) -> OpenState:
    return self.__simulator
  
  @property
  def saif(self) -> OpenState:
    return self.__saif


  @property
  def project_path(self) ->  Path:
    """
    return vivado project path

    Returns
    -------
      Path
    """
    if self.__project_path is None:
      raise PyvadoError("No project path")

    return self.__project_path
  
  @property
  def project_dir(self) -> Path:
    """
    return vivado project directory

    Returns
    -------
      Path
    """
    if self.__project_path is None:
      raise PyvadoError("No project path")

    return self.__project_path.parent
  
  @property
  def project_name(self) -> Path:
    """
    return vivado project name (without .xpr)

    Returns
    -------
      Path
    """
    if self.__project_path is None:
      raise PyvadoError("No project path")

    return self.__project_path.stem
  
  def version(self) -> str:
    """
    get vivado version

    Returns
    -------
    str:
      vivado version
    """

    self.__vivado_process.send("puts [version -short]")
    return self.__vivado_process.read().strip()
  
  def get_parts(self, filter : str = "") -> list[str] : 
    """
    get hardware installed parts
    
    Parameters
    ----------
    filter : str = ""
      part filter

    Returns
    -------
    list[str]
      list of parts
    """

    if filter == "":
      self.__vivado_process.send("puts [get_parts]")
    else:
      filter = filter.replace(' ', '*')
      self.__vivado_process.send(f"puts [get_parts -filter {{NAME =~ \"*{filter}*\"}}]")

    parts = self.__vivado_process.read()
    parts = parts.strip()

    if len(parts) == 0:
      return []
    else:
      return parts.split(' ')
    
  def get_boards(self, filter : str = "") -> list[str] : 
    """
    get installed boards
    
    Parameters
    ----------
    filter : str = ""
      part filter

    Returns
    -------
    list[str]
      list of parts
    """

    if filter == "":
      self.__vivado_process.send("puts [get_boards]")
    else:
      filter = filter.replace(' ', '*')
      self.__vivado_process.send(f"puts [get_boards -filter {{NAME =~ \"*{filter}*\"}}]")

    parts = self.__vivado_process.read()
    parts = parts.strip()

    if len(parts) == 0:
      return []
    else:
      return parts.split(' ')
  