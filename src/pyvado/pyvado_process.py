"""
File name: pyvado_process
Author: aureliesa
Version: 1.0.0
License: GPL-3.0-or-later
Dependencies: subprocess, time, pyvado_error
Descriptions: Vivado subprocess
"""

import subprocess
import time
from .pyvado_error import PyvadoError

class PyvadoProcess:
  """
  Vivado subprocess manager

  Attributes
  ----------

  Methods
  -------
  send(cmd : str | list[str], blocking : bool = True)
    send command line(s) to vivado. If blocking=True, wait for the end of command line execution
  read(self) -> str:
    read vivado output
  close(self):
    close vivado process
  """

  def __init__(
      self, 
      vivado_command : str = "vivado",
      timeout : int  = 600
    ):
    """
    Constructor

    Parameters
    ----------
    vivado_command : str = "vivado"
      vivado launching command line
    timeout : int = 600
      command timeout
    """

    self.__timeout = timeout

    self.__process = subprocess.Popen(
      [vivado_command, "-mode", "tcl", "-log", ".pyvadoLog/vivado.log", "-journal", ".pyvadoLog/vivado.jou"],
      stdin = subprocess.PIPE,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      text = True
    )

    self.__process.stdin.write("puts \"PYVADO_COMMAND_DONE\"\n")
    self.__process.stdin.flush()


    start = time.time()
    while not "PYVADO_COMMAND_DONE" in self.__process.stdout.readline():
      if time.time() - start > self.__timeout:
        raise TimeoutError("Command execution duration has exceed timeout")

    

  def send(self, cmd : str | list[str], blocking : bool = True):
    """
    send command line(s) to vivado. If blocking=True, wait for the end of command line execution

    Parameters
    ----------
    cmd : str | list[str]
      command line(s)
    blocking : bool = True
      wait for the end of command line execution if True
    """

    if self.__process.poll() is not None:
      raise RuntimeError("Vivado has been killed")

    start_time = time.time()

    if isinstance(cmd, list):
      cmd = '\n'.join(cmd)

    self.__process.stdin.write(cmd+'\n')

    if blocking:
      self.__process.stdin.write("puts \"PYVADO_COMMAND_DONE\"\n")

    self.__process.stdin.flush()

    self.__process.stdout.flush()

    if blocking:
      while True:
        
        if time.time() - start_time > self.__timeout:
          raise TimeoutError("Command execution duration has exceed timeout")

        line = self.__process.stdout.readline()

        if "invalid command name" in line:
          raise PyvadoError(line)
        
        if line.startswith("ERROR:"):
          raise PyvadoError(line)

        if line.startswith("PYVADO_COMMAND_DONE"):
          break
  
  def read(self) -> str:
    """
    read vivado output
    """

    return self.__process.stdout.readline()
  
  def close(self):
    """
    close vivado process
    """
    
    self.__process.kill()