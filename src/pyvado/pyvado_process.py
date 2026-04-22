"""
File name: pyvado_process
Author: aureliesa
Version: 1.1.0
License: GPL-3.0-or-later
Dependencies: subprocess, time, pyvado_error
Descriptions: Vivado subprocess
"""

import subprocess
import time
from .pyvado_error import PyvadoError
import os
from pathlib import Path

class PyvadoProcess:
  """
  Vivado subprocess manager

  Attributes
  ----------

  Methods
  -------
  send(cmd : str | list[str])
    send command line(s) to vivado.
  read(self) -> str:
    read vivado output
  close(self):
    close vivado process
  flush():
    flush internal buffer
  """

  __SENTINEL = "PYVADO_COMMAND_DONE"
  __SENTINEL_CMD = f"puts \"{__SENTINEL}\""

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
      
    self.__process.stdin.write("puts [version -short]\n")
    self.__process.stdin.flush()
    version = self.__process.stdout.readline()
    
      
    # Liste de suspects habituels
    search_paths = [
        Path.home() / ".Xilinx/Vivado",
        Path(os.environ.get("XILINX_VIVADO", "/opt/Xilinx/Vivado")),
    ]
    found = []
    for p in search_paths:
        # On cherche n'importe quel dossier nommé 'board_files' ou 'board_store'
        found.extend([str(d) for d in p.rglob("*board_store*") if d.is_dir() and version in str(d)])

    found = ' '.join([f'\"{r}\"' for r in found])
    self.send(f"set_param board.repoPaths [list {found}]")

    self.__buffer = []

  def flush(self):
    """
    flush internal read buffer
    """

    self.__buffer = []

  def send(self, cmd : str | list[str]):
    """
    send command line(s) to vivado.

    Parameters
    ----------
    cmd : str | list[str]
      command line(s)
    """
    self.flush()

    if not isinstance(cmd, list):
      cmd = [cmd]

    for c in cmd:
      self.__run(c)

  def __run(self, cmd : str):
    """
    run vivado command
    """

    if self.__process.poll() is not None:
      raise RuntimeError("Vivado has been killed")

    start_time = time.time()

    self.__process.stdin.write(cmd + '\n')
    self.__process.stdin.write(self.__SENTINEL_CMD + '\n')

    self.__process.stdin.flush()

    self.__process.stdout.flush()

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

      self.__buffer.append(line)

  
  def read(self) -> str:
    """
    read vivado output
    """

    if len(self.__buffer) != 0:
      return self.__buffer.pop(0)
    else:
      return None
  
  def close(self):
    """
    close vivado process
    """
    
    self.__process.kill()