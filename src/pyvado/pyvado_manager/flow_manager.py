"""
File name: flow_manager
Author: aureliesa
Version: 1.1.0
License: GPL-3.0-or-later
Dependencies: pyvado_session, pyvado_manager, pyvado_error
Descriptions: Pyvado synthesis flow manager
"""

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
  set_toplevel(module_name : str)
    setup toplevel
  reset_run(run_name : str = "synth_1")
    reset run
  synthesis(synth_name : str = "synth_1", num_jobs : int = 32)
    Run synthesis
  ooc_syntheses(ooc_module_name : str, extra_option : str = "")
    run out oof contect synthesis
  implementation(impl_name : str = "impl_1", num_jobs : int = 32)
    run implementation
  bitstream(impl_name : str = "impl_1", num_jobs : int = 32)
    run bitstream
  run_all(synth_name : str = "synth_1", impl_name : str = "impl_1", num_jobs : int = 32, reset_before : bool = True)
    run synthesis, implementation and generate bitstream
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
    """
    
    super().__init__(
      pyvado_session = pyvado_session
    )

  def set_toplevel(self, module_name : str):
    """
    setup toplevel
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("project must be open")
    
    self._pyvado_session.process.send([
      f"set_property top {module_name} [current_fileset]",
      "update_compile_order -fileset sources_1",
    ])

  def reset_run(self, run_name : str = "synth_1"):
    """
    reset run

    Parameters
    ----------
    run_name : str = "synth_1"
      run_name to reset
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("project must be open")
    
    if run_name == "":
      raise ValueError("synth name is not set")
    
    self._pyvado_session.process.send(f"reset_runs {run_name}")


  def synthesis(self, synth_name : str = "synth_1", num_jobs : int = 32):
    """
    Run synthesis

    Parameters
    ----------
    synth_name : str = "synth_1"
      synhtesis run name
    num_jobs : int = 32
      number of jobs
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("project must be open")

    if num_jobs < 1:
      raise ValueError("num jobs must be higher or equal than 1")
    
    if synth_name == "":
      raise ValueError("synth name is not set")
    
    self._pyvado_session.process.send([
      f"launch_runs {synth_name} -jobs {num_jobs}", 
      f"wait_on_run {synth_name}"
    ])

  def ooc_syntheses(self, ooc_module_name : str, extra_option : str = ""):
    """
    run out oof contect synthesis

    Parameters
    ----------
    ooc_module_name : str
      module name to synthesis
    extra_option : str
      extra command option
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("Project must be open")
    
    self._pyvado_session.process.send(f"synth_design -top {ooc_module_name} -part [get_property PART [current_project]] -mode out_of_context {extra_option}")

  def implementation(self, impl_name : str = "impl_1", num_jobs : int = 32):
    """
    Run implementation

    Parameters
    ----------
    impl_name : str = "synth_1"
      implementation run name
    num_jobs : int = 32
      number of jobs
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("project must be open")

    if num_jobs < 1:
      raise ValueError("num jobs must be higher or equal than 1")
    
    if impl_name == "":
      raise ValueError("impl name is not set")
    
    self._pyvado_session.process.send([
      f"launch_runs {impl_name} -jobs {num_jobs}", 
      f"wait_on_run {impl_name}"
    ])

  def bitstream(self, impl_name : str = "impl_1", num_jobs : int = 32):
    """
    run bitstream generation

    Parameters
    ----------
    impl_name : str = "impl_1"
      implementation run name
    num_jobs : int = 32
      number of jobs
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("project must be open")

    if num_jobs < 1:
      raise ValueError("num jobs must be higher or equal than 1")
    
    if impl_name == "":
      raise ValueError("impl name is not set")
    
    self._pyvado_session.process.send([
      f"launch_runs {impl_name} -to_step write_bitstream -jobs {num_jobs}",
      f"wait_on_run {impl_name}"
    ])

  def run_all(self, synth_name : str = "synth_1", impl_name : str = "impl_1", num_jobs : int = 32, reset_before : bool = True):
    """
    run all flow

    Parameters
    ----------
    synth_name : str = "synth_1"
      synhtesis run name
    impl_name : str = "impl_1"
      implementation run name
    num_jobs : int = 32
      number of jobs
    """

    if not self._pyvado_session.project.is_open():
      raise PyvadoError("project must be open")

    if num_jobs < 1:
      raise ValueError("num jobs must be higher or equal than 1")
    
    if synth_name == "":
      raise ValueError("synth name is not set")
    
    if impl_name == "":
      raise ValueError("impl name is not set")
    
    if reset_before:
      self.reset_run(run_name=synth_name)

    self.synthesis(synth_name=synth_name, num_jobs=num_jobs)

    self.implementation(impl_name=impl_name, num_jobs=num_jobs)

    self.bitstream(impl_name=impl_name, num_jobs=num_jobs)