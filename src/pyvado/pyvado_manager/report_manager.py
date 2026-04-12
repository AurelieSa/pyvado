"""
File name: report_manager
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: pyvado_process, pyvado_session, pyvado_manager, pyvado_error
Descriptions: Pyvado synthesis flow manager
"""

from ..pyvado_process import PyvadoProcess
from ..pyvado_error import PyvadoError
from ..pyvado_session import PyvadoSession
from .pyvado_manager import PyvadoManager
from pathlib import Path

class ReportManager(PyvadoManager):
  """
  vivado report manager
  
  Attributes
  ----------

  Methods
  -------
  open(run_name : str)
    open run to get reports
  close()
    close runs
  utilisation(output_path : str = ".", hierarchical : bool = True)
    report run utilization
  power(output_path : str = ".")
    report run power consomption
  set_activity(file_path : str, strip_path : str = "")
    Read saif file
  """

  def __init__(self, 
               vivado_process : PyvadoProcess, 
               pyvado_session : PyvadoSession
              ):
    
    super().__init__(
      vivado_process = vivado_process, 
      pyvado_session = pyvado_session
    )

    self.__run = None

  def get_runs(self) -> list[str] :
    """
    get project runs

    Parameters
    ----------

    Returns
    -------
    list[str]
      list of runs

    Errors
    ------
    PyvadoError
      project must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open")

    self._vivado_process.send("puts [get_runs]", blocking=False)

    runs = self._vivado_process.read().strip()

    return runs.split(" ")
  
  def open(self, run_name : str):
    """
    open run to get reports

    Parameters
    ----------
    run_name : str
      run that must be open

    Errors
    ------
    PyvadoError
      vivado project must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open")

    runs = self.get_runs()

    if not run_name in runs:
      raise PyvadoError(f"{run_name} is not available")
    
    self._vivado_process.send(f"open_run {run_name}")

    self.__run = run_name

  def close(self):
    """
    close runs
    """

    if not self.__run is None:
      self._vivado_process.send("close_design")
      self.__run = None

  def utilization(self, output_path : str = ".", hierarchical : bool = True):
    """
    report run utilization

    Parameters
    ----------
    output_path : str = ""
      output file path
    hierarchical : bool = True
      report hierarchical utilization

    Errors
    ------
    PyvadoError
      proejct must be open
    PyvadoError
      run must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open")
    
    if not self.__run:
      raise PyvadoError("Run must be open")
    
    if output_path == ".":
      output_path = "./utilization_report.txt"

    output_path = Path(output_path).resolve()

    if hierarchical:
      self._vivado_process.send(f"report_utilization -hierarchical -file {output_path}")
    else:
      self._vivado_process.send(f"report_utilization -file {output_path}")

  def power(self, output_path : str = "."):
    """
    report run power consomption

    Parameters
    ----------
    output_path : str = ""
      output report path

    Errors
    ------
    PyvadoError
      project must be open
    PyvadoError
      run must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open")
    
    if not self.__run:
      raise PyvadoError("Run must be open")
    
    if output_path == ".":
      output_path = "./power_report.txt"

    output_path = Path(output_path).resolve()

    self._vivado_process.send(f"report_power -file {output_path}")

  def set_activity(self, file_path : str, strip_path : str = ""):
    """
    Read saif file

    Parameters
    ----------
    file_path : str
      saif file path
    strip_path : str = ""
      saif read strip path

    Errors
    ------
    PyvadoError
      project must be open
    PyvadoError
      run must be open
    ValueError
      file does not exist
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open")
    
    if not self.__run:
      raise PyvadoError("Design must be open")
    
    saif_file = Path(file_path).resolve()

    if not saif_file.exists():
      raise ValueError(f"{saif_file} does not exist")
    
    if not saif_file.suffix == ".saif":
      raise ValueError(f"{saif_file} must use .saif extension")
    
    if strip_path == "":
      self._vivado_process.send(f"read_saif {saif_file}")
    else:
      self._vivado_process.send(f"read_saif -strip_path {strip_path} {saif_file}")
