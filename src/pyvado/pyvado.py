"""
File name: pyvado
Author: aureliesa
Version: 1.0.0
License: GPL-3.0-or-later
Dependencies: pyvado_process, pyvado_session, pyvado_manager
Descriptions: Vivado Python API wrapper
"""

from .pyvado_process import PyvadoProcess
from .pyvado_session import PyvadoSession
from .pyvado_manager import *
import os

class Pyvado:
  """
  Python vivado API wrapper
  
  Attributes
  ----------
  session : PyvadoSession
    pyvado session data structure
  project : ProjectManager
    pyvado project manager
  flow : FlowManager
    pyvado synthesis flow manager
  files : FilesManager
    project file manager
  hardware : HardwareManager
    vivado hardware manager
  report : ReportManager
    vivado report manager
  simulator : SimulatorManager
    vivado simulator
  tcl : TCLManager
    direct tcl command
  """

  def __init__(self,
               project_path : str = "",
               vivado_command : str = "vivado",
               process_timeout : int = 600
              ):
    """
    PyVado constructor

    Parameters
    ----------
    project_path : str = ""
      vivado project path
    vivado_command : str = "vivado"
      vivado command line
    process_timeout : int = 600
      vivado command timeout
    """

    if not os.path.exists(".pyvadoLog"):
      os.makedirs(".pyvadoLog")


    

    self.__session = PyvadoSession(
      project_path = project_path,
      vivado_command=vivado_command,
      process_timeout=process_timeout
    )

    self.__project = ProjectManager(
      pyvado_session = self.session
    )

    self.__flow = FlowManager(
      pyvado_session = self.session
    )

    self.__files = FileManager(
      pyvado_session = self.session
    )

    self.__hardware = HardwareManager(
      pyvado_session = self.session
    )

    self.__report = ReportManager(
      pyvado_session = self.session
    )

    self.__simulator = SimulationManager(
      pyvado_session = self.session
    )

    self.__tcl = TCLManager(
      pyvado_session = self.session
    )

  @property
  def session(self) -> PyvadoSession:
    return self.__session

  @property
  def project(self) -> ProjectManager:
    return self.__project

  @property
  def flow(self) -> FlowManager:
    return self.__flow

  @property
  def files(self) -> FileManager:
    return self.__files

  @property
  def hardware(self) -> HardwareManager:
    return self.__hardware

  @property
  def report(self) -> ReportManager:
    return self.__report

  @property
  def simulator(self) -> SimulationManager:
    return self.__simulator
  
  @property
  def tcl(self) -> TCLManager:
    return self.__tcl

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc, tb):

    if self.__session.target.is_open():
      self.hardware.close_target()

    if self.__session.hw_server.is_open():
      self.hardware.disconnect_server()

    if self.__session.hardware.is_open():
      self.hardware.close_hardware()

    if self.__session.project.is_open():
      self.project.close()

    if self.__session.simulator.is_open():
      self.simulator.close()
      
    self.__session.process.close()
