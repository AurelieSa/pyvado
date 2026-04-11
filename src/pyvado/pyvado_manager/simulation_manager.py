"""
File name: flow_manager
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

class SimulationManager(PyvadoManager):
  """
  Vivado Simulation Manager

  Methods
  -------
  open()
    open simulator
  close()
    close simulator
  set_toplevel(module_name : str)
    setup simulation toplevel
  restart()
    restart simulator
  run(duration : str = "all")
    run simulation
  log_saif(output_path : str = ".", scope : str = "")
    log saif activity. If a file is already open, it will be close before
  close_saif()
    close saif file
  """

  def __init__(self, 
               vivado_process : PyvadoProcess, 
               pyvado_session : PyvadoSession
              ):
    
    super().__init__(
      vivado_process = vivado_process, 
      pyvado_session = pyvado_session
    )

    self.__saif_open = False

  def open(self):
    """
    open manager

    Errors
    ------
    PyvadoError
      project must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Vadio project must be open")
    
    self._vivado_process.send("launch_simulation")
    self._pyvado_session.simulator.open()
    self.restart()

  def close(self):
    """
    close vivado simulator
    """

    if self._pyvado_session.simulator.is_open():

      if self.__saif_open:
        self._vivado_process.send("close_saif") # close saif only open by simulator

      self._vivado_process.send("close_sim")
      self._pyvado_session.simulator.close()

      

  def set_toplevel(self, module_name : str):
    """
    set simulation top level

    Attributes
    ----------
    module_name : str
      top level module name

    Errors
    ------
    PyvadoError
      project must be open
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Vivado project must be open")
    
    self._vivado_process.send([
      f"set_property top {module_name} [get_filesets sim_1]",
      "update_compile_order -fileset sources_1",
      "set_property top_lib xil_defaultlib [get_filesets sim_1]"
    ])

  def restart(self):
    """
    restart simuator

    Errors
    ------
    PyvadoError
      simulator must be open
    """

    if not self._pyvado_session.simulator.is_open():
      raise PyvadoError("Simulator must be open")
    
    self._vivado_process.send("restart")

  def run(self, duration : str = "all"):
    """
    run simulation

    Attributes
    ----------
    duration : str = "all"
      simulation duration. Duration must be all or with time units (ps, ns, us, ms, s)
    
    Errors
    PyvadoError
      simulator must be open
    PyvadoError
      duration invalid format
    """

    correct_time_unit = ["ps", "ns", "us", "ms", "s"]

    if not self._pyvado_session.simulator.is_open():
      raise PyvadoError("Simulator must be open")

    if duration != "all" and not any(duration.endswith(unit) for unit in correct_time_unit):
      raise PyvadoError(f"{duration} has no correct format")
    
    self._vivado_process.send(f"run {duration}")

  def log_saif(self, output_path : str = ".", scope : str = ""):
    """
    log saif activity. If a file is already open, it will be close before

    Attributes
    ----------
    output_path : str = "."
      output saif file
    scope : str = ""
      scope log

    Errors
    ------
    PyvadoError
      simulator must be open
    ValueError
      output path must be saif format
    """

    if not self._pyvado_session.simulator.is_open():
      raise PyvadoError("Simulator must be open")
    
    if output_path == ".":
      output_path = "./saif_activity.saif"
    
    output_path = Path(output_path).resolve()

    if output_path.suffix != ".saif":
      raise ValueError(f"Bad extension file")
    
    if self._pyvado_session.saif.is_open():
      self.close_saif()
    
    cmd = [f"open_saif {output_path}"]

    if scope != "":
      cmd.append(f"log_saif [get_objects -r /{scope}/*]")
    else:
      cmd.append(f"log_saif [get_objects -r *]")
    

    self._vivado_process.send(cmd=cmd)

    self._pyvado_session.saif.open()
    self.__saif_open = True

  def close_saif(self):
    """
    close saif file
    """

    if self._pyvado_session.saif.is_open():
      self._vivado_process.send("close_saif")
      self._pyvado_session.saif.close()
      self.__saif_open = False
