"""
File name: hardware_manager
Author: aureliesa
Version: 1.0.0
License: GPL-3.0-or-later
Dependencies: pyvado_process, pyvado_session, pyvado_manager, pyvado_error, pathlib
Descriptions: Pyvado synthesis flow manager
"""

from .pyvado_manager import PyvadoManager
from ..pyvado_process import PyvadoProcess
from ..pyvado_session import PyvadoSession
from ..pyvado_error import PyvadoError
from pathlib import Path

class HardwareManager(PyvadoManager):
  """
  Hardware Manager

  Attributes
  ----------

  Methods
  -------
  open_hardware()
    open vivado hardware manager
  close_hardware()
    close vivado hardware manager
  connect_server(url : str = "")
    connect to hardware server
  disconnect_server()
    disconnect to hardware server
  open_target()
    open target device
  close_target()
    close target device
  set_bitstream(bitstream_path : str = "")
    setup bitstream file
  program_device()
    send bitstream to opened hardware target *
  deploy(bitstream_path : str = "", server_url : str = "")
    Completly deploy bitstream on FPGA from open hardware to device programming
  """

  def __init__(self, 
               vivado_process : PyvadoProcess, 
               pyvado_session : PyvadoSession
              ):
    
    super().__init__(
      vivado_process=vivado_process, 
      pyvado_session=pyvado_session
    )

  def open_hardware(self):
    """
    open hardware manager
    """

    self._vivado_process.send("open_hw_manager")
    self._pyvado_session.hardware.open()

  def close_hardware(self):
    """
    close hardware manager
    """

    if self._pyvado_session.hardware.is_open():
      self._vivado_process.send("close_hw_manager")
      self._pyvado_session.hardware.close()

  def connect_server(self, url : str = ""):
    """
    connect to hardware server

    Parameters
    ----------
    url : str = ""
      hardware server url

    Raises
    ------
    PyvadoError
      If vivado hardware manager is not open
    """

    if not self._pyvado_session.hardware.is_open():
      raise PyvadoError("Vivado hardware manager must be open")

    if url == "":
      cmd = "connect_hw_server"
    else:
      cmd = f"connect_hw_server -url {url}"

    self._vivado_process.send(cmd=cmd)
    self._pyvado_session.hw_server.open()

  def disconnect_server(self):
    """
    disconnect from hardwaer server
    """

    if self._pyvado_session.hw_server.is_open():
      self._vivado_process.send("disconnect_hw_server")
      self._pyvado_session.hw_server.close()


  def open_target(self):
    """
    open hardware manager

    Raises
    ------
    PyvadoError
      If vivado hardware server is not connected
    """
    if not self._pyvado_session.hw_server.is_open():
      raise PyvadoError("Vivado hardware manager and hardware server must be open")
    
    self._vivado_process.send("open_hw_target")
    self._pyvado_session.target.open()

  def close_target(self):
    """
    close hardware manager
    """

    if self._pyvado_session.target.is_open():
      self._vivado_process.send("close_hw_target")
      self._pyvado_session.target.close()

  def set_bitstream(self, bitstream_path : str = ""):
    """
    setup bitstream file

    Parameters
    ----------
    bitstream_path : str = ""
      bitstream file path, automatically detected if project is open

    Raises
    ------
    PyvadoError
      If hardware target is not open
    PyvadoError
      No bitstream generated
    PyvadoError
      bitstream path not provided and project is close
    ValueError
      If bitstream path does not finish with .bit extension
    PyvadoError
      If bitstream file deos not exist
    """

    if not self._pyvado_session.target.is_open():
      raise PyvadoError("Hardware target must be open")
    
    if bitstream_path == "":
      if self._pyvado_session.project.is_open():
        self._vivado_process.send("puts [get_property DIRECTORY [current_run -implementation]]", blocking=False)
        toplevel_path = self._vivado_process.read().strip()
        
        bitstream_files = list(Path(f"{toplevel_path}/").glob("*.bit"))

        if bitstream_files:
          bitstream_path = bitstream_files[0]
        else:
          raise PyvadoError(f"No bitstream found in {toplevel_path}")
      else:
        raise PyvadoError("Bitstream path requiered if no project open")

    bitstream_path = Path(bitstream_path).resolve()

    if bitstream_path.suffix != ".bit":
      raise ValueError("wrong bitstream format")

    if not bitstream_path.exists():
      raise PyvadoError(f"{bitstream_path} does not exist")

    self._vivado_process.send(f"set_property PROGRAM.FILE {{{bitstream_path}}} [current_hw_device]")

  def program_device(self):
    """
    send bitstream to the hardware target

    Raises
    ------
    PyvadoError
      If hardware target is not open
    """

    if not self._pyvado_session.target.is_open():
      raise PyvadoError("No hardware target to programm")
    
    self._vivado_process.send("program_hw_devices [current_hw_device]")

  def deploy(self, bitstream_path : str = "", server_url : str = ""):
    """
    Completly deploy bitstream on FPGA from open hardware to device programming

    Parameters
    ----------
    bitstream_path : str = ""
      bitstream file path, automatically detect if project is open
    server_url : str = ""
      hardware server url
    """

    if not self._pyvado_session.hardware.is_open():
      self.open_hardware()

    if not self._pyvado_session.hw_server.is_open():
      self.connect_server(url=server_url)

    if not self._pyvado_session.target.is_open():
      self.open_target()

    self.set_bitstream(bitstream_path=bitstream_path)

    self.program_device()

