
import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError
import os

class TestPyvadoCommand(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_session_correctly_setup(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    with self.assertRaises(ValueError):
      pv =  Pyvado("foo/bar.xdc")
    

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_enter(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    with Pyvado("foo/bar.xpr") as pv:
      self.assertIsInstance(pv, Pyvado)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_exit_close_process(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    with Pyvado("foo/bar.xpr") as pv:
      self.assertIsInstance(pv, Pyvado)

    self.assertTrue(mock_proc.kill.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_exit_close_everything(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    with Pyvado("foo/bar.xpr") as pv:
      pv.project.open()
      pv.hardware.open_hardware()
      pv.hardware.connect_server()
      pv.hardware.open_target()
      pv.simulator.open()

    self.assertTrue(mock_proc.kill.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("close_project" in s for s in calls))
    self.assertTrue(any("close_hw" in s for s in calls))
    self.assertTrue(any("disconnect_hw_server" in s for s in calls))
    self.assertTrue(any("close_hw_target" in s for s in calls))
    self.assertTrue(any("close_sim" in s for s in calls))
