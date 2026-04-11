"""
File name: pyvado_error
Author: aureliesa
Version: 0.1.0
License: GPL-3.0-or-later
Contact: aurelie.saulq@proton.me
Dependencies: 
Descriptions: Pyvado error
"""

class PyvadoError(Exception):
  """
  Pyvado internal error class

  Attributes
  ----------
  
  Methods
  -------
  """

  def __init__(self, message : str):
    super().__init__(message)