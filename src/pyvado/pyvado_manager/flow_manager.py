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

class FlowManager(PyvadoManager):
  """
  Pyvado synthesis flow manager

  Attributes
  ----------

  Methods
  -------
  reset_run(run_name : str = "synth_1")
    reset run
  run_synthesis(synth_name : str = "synth_1", num_jobs : int = 32)
    Run synthesis
  run_implementation(impl_name : str = "impl_1", num_jobs : int = 32)
    run implementation
  run_bitstream(impl_name : str = "impl_1", num_jobs : int = 32)
    run bitstream
  """

  def __init__(self,
               vivado_process : PyvadoProcess,
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
    """
    
    super().__init__(
      vivado_process = vivado_process,
      pyvado_session = pyvado_session
    )

  def reset_run(self, run_name : str = "synth_1"):
    """
    reset run

    Parameters
    ----------
    run_name : str = "synth_1"
      run_name to reset
    """

    if not self._pyvado_session.is_project_open():
      raise PyvadoError("project must be open")
    
    if run_name == "":
      raise ValueError("synth name is not set")
    
    self._vivado_process.send(f"reset_run {run_name}")


  def run_synthesis(self, synth_name : str = "synth_1", num_jobs : int = 32):
    """
    Run synthesis

    Parameters
    ----------
    synth_name : str = "synth_1"
      synhtesis run name
    num_jobs : int = 32
      number of jobs
    """

    if not self._pyvado_session.is_project_open():
      raise PyvadoError("project must be open")

    if num_jobs < 1:
      raise ValueError("num jobs must be higher or equal than 1")
    
    if synth_name == "":
      raise ValueError("synth name is not set")
    
    self._vivado_process.send([
      f"launch_runs {synth_name} -jobs {num_jobs}", 
      f"wait_on_run {synth_name}"
    ])

  def run_implementation(self, impl_name : str = "impl_1", num_jobs : int = 32):
    """
    Run implementation

    Parameters
    ----------
    impl_name : str = "synth_1"
      implementation run name
    num_jobs : int = 32
      number of jobs
    """

    if not self._pyvado_session.is_project_open():
      raise PyvadoError("project must be open")

    if num_jobs < 1:
      raise ValueError("num jobs must be higher or equal than 1")
    
    if impl_name == "":
      raise ValueError("impl name is not set")
    
    self._vivado_process.send([
      f"launch_runs {impl_name} -jobs {num_jobs}", 
      f"wait_on_run {impl_name}"
    ])

  def run_bitstream(self, impl_name : str = "impl_1", num_jobs : int = 32):
    """
    run bitstream generation

    Parameters
    ----------
    impl_name : str = "impl_1"
      implementation run name
    num_jobs : int = 32
      number of jobs
    """

    if not self._pyvado_session.is_project_open():
      raise PyvadoError("project must be open")

    if num_jobs < 1:
      raise ValueError("num jobs must be higher or equal than 1")
    
    if impl_name == "":
      raise ValueError("impl name is not set")
    
    self._vivado_process.send([
      f"launch_runs {impl_name} -to_step write_bitstream -jobs {num_jobs}",
      f"wait_on_run {impl_name}"
    ])