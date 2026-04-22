"""
File name: report_manager
Author: aureliesa
Version: 1.2.0
License: GPL-3.0-or-later
Dependencies: pyvado_session, pyvado_manager, pyvado_error, pathlib
Descriptions: Pyvado synthesis flow manager
"""

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
  utilisation(output_path : str = ".", extra_option : str = "")
    report utilization
  power(output_path : str = ".", extra_option : str = "")
    report power consomption
  clock_network(output_path : str = ".", extra_option : str = "")
    report clock network
  timing(output_path : str = ".", extra_option : str = "")
    report timing
  methodology(output_path : str = ".", extra_option : str = "")
    report methodology
  drc(output_path : str = ".", extra_option : str = "")
    report drc
  noise(output_path : str = ".", extra_option : str = "")
    report noise
  operating_conditions(output_path : str = ".", extra_option : str = "")
    report operating conditions
  set_activity(file_path : str, strip_path : str = "")
    Read saif file
  """

  def __init__(self, 
               pyvado_session : PyvadoSession
              ):
    
    super().__init__(
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

    self._pyvado_session.process.send("puts [get_runs]")

    runs = self._pyvado_session.process.read().strip().split(" ")

    available_run = []
    for run in runs:
      self._pyvado_session.process.send(f"puts [get_property STATUS [get_runs {run}]]")
      status = self._pyvado_session.process.read().strip()
      if status != "Not started":
        available_run.append(run)

    return available_run
  
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
    
    self._pyvado_session.process.send(f"open_run {run_name}")

    self.__run = run_name

  def close(self):
    """
    close runs
    """

    if not self.__run is None:
      self._pyvado_session.process.send("close_design")
      self.__run = None

  def utilization(self, output_path : str = ".", extra_option : str = ""):
    """
    report utilization

    Parameters
    ----------
    output_path : str = ""
      output file path
    extra_option : str = ""
      extra command option

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

    self._pyvado_session.process.send(f"report_utilization {extra_option} -file {output_path}")

  def power(self, output_path : str = ".", extra_option : str = ""):
    """
    report power consomption

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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

    self._pyvado_session.process.send(f"report_power {extra_option} -file {output_path}")

  def timing(self, output_path : str = ".", extra_option : str = ""):
    """
    report timing

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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
      output_path = "./timing_report.txt"

    output_path = Path(output_path).resolve()

    self._pyvado_session.process.send(f"report_timing_summary {extra_option} -file {output_path}")

  def clock_network(self, output_path : str = ".", extra_option : str = ""):
    """
    report clock network

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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
      output_path = "./clock_network_report.txt"

    output_path = Path(output_path).resolve()

    self._pyvado_session.process.send(f"report_clock_network {extra_option} -file {output_path}")

  def clock_interaction(self, output_path : str = ".", extra_option : str = ""):
    """
    report clock interaction

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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
      output_path = "./clock_interaction_report.txt"

    output_path = Path(output_path).resolve()

    self._pyvado_session.process.send(f"report_clock_interaction {extra_option} -file {output_path}")

  def methodology(self, output_path : str = ".", extra_option : str = ""):
    """
    report methodology

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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
      output_path = "./methodology_report.txt"

    output_path = Path(output_path).resolve()

    self._pyvado_session.process.send(f"report_methodology {extra_option} -file {output_path}")

  def drc(self, output_path : str = ".", extra_option : str = ""):
    """
    report drc

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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
      output_path = "./drc_report.txt"

    output_path = Path(output_path).resolve()

    self._pyvado_session.process.send(f"report_drc {extra_option} -file {output_path}")

  def noise(self, output_path : str = ".", extra_option : str = ""):
    """
    report noise

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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
      output_path = "./noise_report.txt"

    output_path = Path(output_path).resolve()

    self._pyvado_session.process.send(f"report_ssn {extra_option} -file {output_path}")

  def operating_conditions(self, output_path : str = ".", extra_option : str = ""):
    """
    report operating conditions

    Parameters
    ----------
    output_path : str = ""
      output report path
    extra_option : str = ""
      extra command option

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
      output_path = "./operating_conditions_report.txt"

    output_path = Path(output_path).resolve()

    self._pyvado_session.process.send(f"report_operating_conditions {extra_option} -file {output_path}")

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
      self._pyvado_session.process.send(f"read_saif {saif_file}")
    else:
      self._pyvado_session.process.send(f"read_saif -strip_path {strip_path} {saif_file}")
