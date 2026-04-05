
import unittest
from unittest.mock import MagicMock, patch
from pyvado.vivadoProcess import VivadoProcess
import sys

class TestVivadoProcess(unittest.TestCase):

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_internal_writing(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    vp = VivadoProcess()
    vp.send("my_cmd")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertIn("my_cmd\n", calls)
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)
    self.assertTrue(any("PYVADO_COMMAND_DONE" in s for s in calls))



  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_send_block_true(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    vp = VivadoProcess()
    vp.send("my_cmd")

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)
    self.assertTrue(any("PYVADO_COMMAND_DONE" in s for s in calls))


  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_send_block_false(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    vp = VivadoProcess()
    vp.send("my_cmd", blocking=False)

    self.assertFalse(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    
    self.assertNotIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)
    self.assertFalse(any("PYVADO_COMMAND_DONE" in s for s in calls))

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  @patch('pyvado.vivadoProcess.time.time')
  def test_send_timeout(self, mock_time, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_time.side_effect = [0, 70]

    mock_proc.stdout.readline.return_value = "working...\n"
    mock_proc.poll.return_value = None

    vp = VivadoProcess(timeout=60)
    
    with self.assertRaises(TimeoutError):
      vp.send("my_cmd", blocking=True)

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_send_process_killed(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = 1

    vp = VivadoProcess()
    
    with self.assertRaises(RuntimeError):
      vp.send("my_cmd", blocking=True)

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_read(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "some results\n"
    mock_proc.poll.return_value = None

    vp = VivadoProcess()
    
    self.assertEqual(vp.read(), "some results\n")

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    vp = VivadoProcess()
    vp.close()

    mock_proc.kill.assert_called_once()
    self.assertTrue(mock_proc.kill.called)