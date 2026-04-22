"""
File name: project_manager
Author: aureliesa
Version: 1.2.0
License: GPL-3.0-or-later
Dependencies: pyvado_session, pyvado_manager, pyvado_error
Descriptions: Pyvado project manager
"""

from ..pyvado_session import PyvadoSession
from .pyvado_manager import PyvadoManager
from ..pyvado_error import PyvadoError
from pathlib import Path

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
      pyvado_session = pyvado_session
    )

  def open(self, project_path : str = ""):
    """
    Open vivado project
    """

    if project_path != "":
      self._pyvado_session.set_project_path(project_path)

    self._pyvado_session.process.send(
      cmd = f"open_project {self._pyvado_session.project_path}"
    )
    self._pyvado_session.project.open()

  def close(self):
    """
    close vivado project
    """
    
    if self._pyvado_session.project.is_open():
      self._pyvado_session.process.send(
        cmd = "close_project"
      )
      self._pyvado_session.project.close()

  def create(self, project_path : str, project_name : str, part : str = None, board : str = None, target_language : str = "VHDL", simulator_language : str = "VHDL"):
    """
    Create vivado project

    Parameters
    ----------
    project_path : str
      vivado project creation path
    project_name : str
      vivado project name
    part : str = None
      hardware part. can be approximative name
    board : str = None
      target board. Can be approximative name
    target_language : str = "VHDL"
      hardware description language
    simulator_language : str = "VHDL"
      simulator hardware description language

    Errors
    ------
    ValueError:
      if project path does not exist
    ValueError:
      if project_path is not a directory
    ValueError:
      if part and board are None
    ValueError:
      if part and board are not None
    """

    project_path = Path(project_path).resolve()

    if not project_path.exists():
      raise ValueError(f"{project_path} does not exist")

    if not project_path.is_dir():
      raise ValueError(f"{project_path} is not a directoy")
    
    path = project_path.joinpath(Path(project_name)).as_posix()

    if part is None and board is None:
      raise ValueError("at least part or bord must be defined")
    
    if part is not None and board is not None:
      raise ValueError("only define part or board")
  
    
    if part is not None:
      hw_given = part
      installed_hw = self._pyvado_session.get_parts(filter=part)
    else:
      hw_given = board
      installed_hw = self._pyvado_session.get_boards(filter=board)


    if len(installed_hw) == 0:
      raise PyvadoError(f"{hw_given} not found")
    
    if len(installed_hw) != 1:
      s = "Multiple hardware found, please select the one you want: \n" + '\n'.join([f"{i}. {installed_hw[i]}" for i in range(len(installed_hw))])
      print(s)
      hw_index = int(input("index :"))
    else:
      hw_index = 0

    hw_given = installed_hw[hw_index]

    self._pyvado_session.process.send(f"create_project {project_name} {path} -force")
    self._pyvado_session.process.send([
      f"set_property target_language {target_language} [current_project]",
      f"set_property simulator_language {simulator_language} [current_project]"
    ])

    if part is None:
      self._pyvado_session.process.send(f"set_property board_part {hw_given} [current_project]", blocking=False)
      
      while True:
        if "Project part" in (s:=self._pyvado_session.process.read()):
          part = s[s.find('(')+1:s.find(')')]
          break

      self._pyvado_session.process.send(f"set_property part {part} [current_project]")
      self._pyvado_session.process.send(f"set_property board_part {hw_given} [current_project]")
    else:
      self._pyvado_session.process.send(f"set_property part {part} [current_project]")

    self._pyvado_session.set_project_path(f"{path}/{project_name}.xpr")
    self._pyvado_session.project.open()
