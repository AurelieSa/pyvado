"""
File name: file_manager
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: pyvado_process, pyvado_session, pyvado_manager, pyvado_error, pathlib, shlex
Descriptions: Pyvado synthesis flow manager
"""

from .pyvado_manager import PyvadoManager
from ..pyvado_process import PyvadoProcess
from ..pyvado_session import PyvadoSession
from ..pyvado_error import PyvadoError
from pathlib import Path
import shlex

class FileManager(PyvadoManager):
  """
  File system manager

  Attributes
  ----------
  SUPPORTED_FILE_EXTENSIONS : list[str] (static)
    list of supported file extensions
  
  Methods
  -------
  add_file(file_path : str, synth_only : bool = False, sim_only : bool = False, import_file : bool =False, force : bool =True)
    Add file on vivado project. Function detect if the file is a constraint file
  add_simulation_file(file_path : str, import_file : bool = False, force : bool = True)
    Add simulation only file
  add_constraint_file(file_path : str, import_file : bool = False, force : bool = True)
    Add constraint file
  remove_file(file_name : str, delete_from_disk : bool = False)
    Remove file from vivado project
  get_files() -> list[str]
    get files from vivado project
  """

  SUPPORTED_FILE_EXTENSIONS = [
    ".nky", ".nkz", ".dcp", ".vho", ".vhd", 
    ".vhdl", ".vhf", ".vhdp", ".sv", ".svp", 
    ".v", ".veo", ".svo", ".vf", ".verilog", 
    ".vr", ".vg", ".vb", ".tf", ".vlog", 
    ".vp", ".vm", ".sveo", ".veo", ".svo"
    ".vh", ".h", ".svh", ".vhp", ".svhp",
    ".edn", ".edf", ".edif", ".ngc", ".bnx",
    ".bmm", ".mif", ".mem", ".bd", ".wcfg", 
    ".coe", ".sdc", ".xdc", ".tcl"
  ]

  def __init__(self, 
               vivado_process : PyvadoProcess, 
               pyvado_session : PyvadoSession
              ):
    """
    Pyvado file manager

    Parameters
    ----------
    vivado_process : PyvadoProcess
      vivado process
    pyvado_session : PyvadoSession
      pyvado project session 
    """

    super().__init__(
      vivado_process = vivado_process, 
      pyvado_session = pyvado_session
    )

  def add_file(self, file_path : str, synth_only : bool = False, sim_only : bool = False, import_file : bool =False, force : bool =True):
    """
    Add file on vivado project. Function detect if the file is a constraint file

    Parameters
    ----------
    file_path : str
      path of file to add
    synth_only : bool
      the added file will be only available for synthesis
    sim_only : bool
      the added file will be only available for simulation
    import_file : bool
      the added file will be copy in the vivado project repo
    force : bool
      force the file to be add if the file already exist
    """

    if synth_only and sim_only:
      raise ValueError("a file must be at least in simulation or synthesis")
    
    if not self._pyvado_session.is_project_open():
      raise PyvadoError("Project must be open to add files")
    
    file_path = Path(file_path).resolve()

    if file_path.suffix not in self.SUPPORTED_FILE_EXTENSIONS:
      raise PyvadoError(f"{file_path.suffix} is not supported")

    cmd = []

    if file_path.suffix == ".xdc":
      if import_file:
        cmd.append(f"import_files -fileset constrs_1 -norecurse{' -force' if force else ''} {file_path}")
      else:
        cmd.append(f"add_files -fileset constrs_1 -norecurse{' -force' if force else ''} {file_path}")
    else:
      if import_file:
        cmd.append(f"import_files -norecurse{' -force' if force else ''} {file_path}")
      else:
        cmd.append(f"add_files -norecurse{' -force' if force else ''} {file_path}")

      cmd.append("update_compile_order")

      if synth_only:
        cmd.append(f"set_property used_in_simulation false [get_files {file_path}]")
      elif sim_only:
        cmd.append(f"set_property used_in_synthesis false [get_files {file_path}]")

    self._vivado_process.send(
      cmd = cmd,
      blocking = True
    )

  def add_simulation_file(self, file_path : str, import_file : bool = False, force : bool = True):
    """
    Add simulation only file

    Parameters
    ----------
    file_path : str
      path of file to add
    import_file : bool
      the added file will be copy in the vivado project repo
    force : bool
      force the file to be add if the file already exist
    """
    
    self.add_file(
      file_path=file_path,
      synth_only=False,
      sim_only=True,
      import_file=import_file,
      force=force
    )

  def add_constraint_file(self, file_path : str, import_file : bool = False, force : bool = True):
    """
    Add constraint file

    Parameters
    ----------
    file_path : str
      path of file to add
    import_file : bool
      the added file will be copy in the vivado project repo
    force : bool
      force the file to be add if the file already exist
    """
    
    sfx = Path(file_path).suffix
    if sfx != ".xdc" and  sfx != ".sdc":
      raise ValueError(f"{sfx} constrainst file extension must be xdc or sdc")
    
    self.add_file(
      file_path=file_path,
      synth_only=False,
      sim_only=False,
      import_file=import_file,
      force=force  
    )

  def remove_file(self, file_name : str, delete_from_disk : bool = False):
    """
    remove file from vivado project

    Parameters
    ----------
    file_name : str
      name of file to remove
    delete_from_disk : bool = False
      if file has been imported into the vivado project, set to true to delete this copy.
    """

    if not self._pyvado_session.is_project_open():
      raise PyvadoError("Project must be open to add files")
    
    cmd = [f"remove_files {file_name}"]

    if delete_from_disk:
      proj_source = f"{self._pyvado_session.get_project_name()}.srcs/"
      files = self.get_files()
      for f in files:
        if proj_source in str(f):
          cmd.append(f"file delete -force {f}")
          break

    cmd.append("update_compile_order")

    self._vivado_process.send(cmd=cmd)

  def get_files(self) -> list[str]:
    """
    get files in vivado project

    Returns
    -------
    list[str]
      list of files
    """

    if not self._pyvado_session.is_project_open():
      raise PyvadoError("Project must be open to add files")

    self._vivado_process.send("puts [get_files]", blocking=False)
    files = self._vivado_process.read()

    return shlex.split(files)