
import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError
import os

class TestPyvadoCommand(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_non_blocking_command(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.run_command("foo_command", blocking = False)


    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn("foo_command\n", calls)
    self.assertNotIn("PYVADO_COMMAND_DONE\n", calls)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_blocking_command(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.run_command("foo_command", blocking = True)

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn("foo_command\n", calls)
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)
    self.assertTrue(any("PYVADO_COMMAND_DONE" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_read(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "some results\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    self.assertEqual(pv.read_output(), "some results\n")