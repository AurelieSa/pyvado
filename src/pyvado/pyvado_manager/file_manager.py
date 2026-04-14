"""
File name: file_manager
Author: aureliesa
Version: 1.0.0
License: GPL-3.0-or-later
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
  add_file(file_path : str | list[str], used_in_synth : bool = True, used_in_sim : bool = True, import_file : bool =False, force : bool =True)
    Add file(s) on vivado project. Function detect if the file is a constraint file
  change_property(file_path : str | list[str], used_in_synth : bool = True, used_in_sim : bool = True)
    change file property
  add_directory(directory_path : str, used_in_synth : bool = True, used_in_sim : bool = True, import_file : bool =False, force : bool =True)
    Add all files in directory and subdirectory
  add_simulation_file(self, file_path : str, import_file : bool = False, force : bool = True)
    Add simulation only file
  add_constraint_file(file_path : str, import_file : bool = False, force : bool = True)
    Add constraint file
  remove_file(file_name : str, delete_from_disk : bool = False)
    remove file from vivado projectt
  get_files(self) -> list[str]
    get files in vivado project
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

  def add_file(self, file_path : str | list[str], used_in_synth : bool = True, used_in_sim : bool = True, import_file : bool =False, force : bool =True):
    """
    Add file(s) on vivado project. Function detect if the file is a constraint file

    Parameters
    ----------
    file_path : str | [str]
      path of file to add
    used_in_synth : bool = Trie
      the added file will be available for synthesis
    used_in_sim : bool = True
      the added file will be available for simulation
    import_file : bool = False
      the added file will be copy in the vivado project repo
    force : bool = True+
      force the file to be add if the file already exist

    Errors
    ------
    ValueError
      file must be available at least for synhtesis or simulation
    PyvadoError
      project is not open
    """

    if not used_in_synth and not used_in_sim:
      raise ValueError("a file must be at least in simulation or synthesis")
    
    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open to add files")
    
    if not isinstance(file_path, list):
      file_path = [file_path]

    design_files = []
    constrainst_files = []

    file_path = [Path(f).resolve() for f in file_path]
    
    for f in file_path:

      if not f.suffix in self.SUPPORTED_FILE_EXTENSIONS:
        raise PyvadoError(f"{f.suffix} extension is not supported")

      if not f.exists():
        raise PyvadoError(f"{f} does not exists")
      
      if f.suffix == ".xdc" or f.suffix == ".sdc":
        constrainst_files.append(str(f))
      else:
        design_files.append(str(f))

    force = '-force' if force else ''
    file = "import_files" if import_file else "add_files"

    cmd = []
      
    if design_files != []:
      files = ' '.join(design_files)
      cmd.append(f"{file} -norecurse {force} {files}")
    
    if constrainst_files != []:
      files = ' '.join(constrainst_files)
      cmd.append(f"{file} -fileset constrs_1 -norecurse {force} {files}")


    cmd.append("update_compile_order")


    self._vivado_process.send(
      cmd = cmd,
      blocking = True
    )

    if design_files != []:
      files = self.get_files()

      file_name = [f.name for f in file_path]

      new_files = ' '.join([f for f in files if Path(f).resolve().name in file_name and not Path(f).suffix in [".xdc", ".sdc"] ])

      self._vivado_process.send(cmd=[
        f"set_property used_in_synthesis {used_in_synth} [get_files {{{new_files}}}]",
        f"set_property used_in_simulation {used_in_sim} [get_files {{{new_files}}}]"
      ])

  def change_property(self, file_path : str | list[str], used_in_synth : bool = True, used_in_sim : bool = True):
    """
    change file property

    Parameters
    ----------
    file_path : str | list[str]
      file path
    used_in_synth : bool = True
      file will be available for synthesis
    used_in_sim : bool = True
      file  will be available for simulation

    Errors
    ------
    ValueError
      file must be available at least for synhtesis or simulation
    PyvadoError
      project is not open
    """

    if not used_in_synth and not used_in_sim:
      raise ValueError("a file must be at least in simulation or synthesis")
    
    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open to add files")

    files = self.get_files()

    if not isinstance(file_path, list):
      file_path = [file_path]

    file_path = [Path(f).resolve() for f in file_path]

    if any(f.suffix == ".xdc" for f in file_path):
      return

    for f in file_path:
      if not str(f) in files:
        raise PyvadoError(f"{f} is not into the project")
      
    files = ' '.join([f.as_posix() for f in file_path])
    
    self._vivado_process.send([
      f"set_property used_in_synthesis {used_in_synth} [get_files {{{files}}}]",
      f"set_property used_in_simulation {used_in_sim} [get_files {{{files}}}]"
    ])

  def add_directory(self, directory_path : str, used_in_synth : bool = True, used_in_sim : bool = True, import_file : bool =False, force : bool =True):
    """
    Add all files in directory and subdirectory

    Parameters
    ----------
    directory_path : str
      directoy path
    used_in_synth : bool = True
      files will be available for synthesis
    used_in_sim : bool = Truee
      files will be available for simulation
    import_file : bool = False
      files will be copy on loval project
    force : bool = True
      if files already exist, files will be replace

    Errors
    ------
    ValueError
      directory path deos not exist
    ValueError
      directory_path is not a directory
    """

    directory_path = Path(directory_path).resolve()

    if not directory_path.exists():
      raise ValueError(f"{directory_path} does not exist")
    
    if not directory_path.is_dir():
      raise ValueError(f"{directory_path} is not a directory")
    
    files = [f for f in directory_path.rglob("*") if f.is_file() and f.suffix in self.SUPPORTED_FILE_EXTENSIONS]

    self.add_file(file_path=files, used_in_synth=used_in_synth, used_in_sim=used_in_sim, force=force, import_file=import_file)  

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
      used_in_synth=False,
      used_in_sim=True,
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

    Errors
    ------
    ValueError
      extension must be .xdc or .sdc
    """
    
    sfx = Path(file_path).suffix
    if sfx != ".xdc" and  sfx != ".sdc":
      raise ValueError(f"{sfx} constrainst file extension must be xdc or sdc")
    
    self.add_file(
      file_path=file_path,
      used_in_sim=True,
      used_in_synth=True,
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

    Errors
    ------
    PyvadoError
      vivado project must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open to add files")
    
    cmd = [f"remove_files {file_name}"]

    if delete_from_disk:
      proj_source = f"{self._pyvado_session.project_name}.srcs/"
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

    Errors
    ------
    PyvadoError
      vivado project must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open to add files")

    self._vivado_process.send("puts [get_files]", blocking=False)
    files = self._vivado_process.read()

    if "No files matched" in files:
      return []

    return shlex.split(files)