
from ..pyvado_process import PyvadoProcess
from ..pyvado_session import PyvadoSession

class PyvadoManager():

  def __init__(self,
               vivado_process : PyvadoProcess,
               pyvado_session : PyvadoSession
              ):
    self._vivado_process = vivado_process
    self._pyvado_session = pyvado_session