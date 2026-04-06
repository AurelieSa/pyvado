"""
File name: pyvado_session
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: pathlib
Descriptions: Vivado Python API wrapper
"""

from pathlib import Path

class PyvadoSession():
  """
  Pyvado project session to store global project informations

  Attributes
  ----------

  Methods
  -------
  is_project_open() -> bool
    return if vivado project is open or not
  open_project()
    signal to session that project is open
  close_project()
    signal to session that project is close
  get_project_path() ->  Path
    return project path
  get_project_dir() -> Path
    return project directory
  get_project_name() -> Path
    return project name (without .xpr)
  """

  def __init__(self,
               project_path : str
              ):
    """
    Class Constructor

    Parameters
    ----------
    project_path : str
      vivado project path. Must finish by xpr extension
    """
    
    if project_path == "" or project_path is None:
      raise ValueError("no project path") 
    
    self.__project_path = Path(project_path).resolve()

    if self.__project_path.suffix != ".xpr":
      raise ValueError("project name must finish with xpr extension")
    
    self.__is_project_open = False

  def is_project_open(self) -> bool:
    """
    return if vivado project is open or not

    Returns
    -------
      bool
    """
    return self.__is_project_open
  
  def open_project(self):
    """
    signal to session that project is open
    """
    
    self.__is_project_open = True

  def close_project(self):
    """
    signal to session that project is close
    """

    self.__is_project_open = False

  def get_project_path(self) ->  Path:
    """
    return vivado project path

    Returns
    -------
      Path
    """

    return self.__project_path
  
  def get_project_dir(self) -> Path:
    """
    return vivado project directory

    Returns
    -------
      Path
    """

    return self.__project_path.parent
  
  def get_project_name(self) -> Path:
    """
    return vivado project name (without .xpr)

    Returns
    -------
      Path
    """

    return self.__project_path.stem
  