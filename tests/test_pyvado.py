
import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado
import os

class TestPyvado(unittest.TestCase):

  def test_project_creation(self):
    

    with self.assertRaises(ValueError):
      pv = Pyvado(
        project_path = "foo",
        project_name = "goo"
      )

    with self.assertRaises(ValueError):
      pv = Pyvado(
        project_path = "foo",
        project_name = "gooxdc"
      )

    with self.assertRaises(ValueError):
      pv = Pyvado(
        project_path = "",
        project_name = "goo.xdc"
      )

    pv = Pyvado(
        project_path = "foo",
        project_name = "goo.xdc"
      )
    self.assertTrue(True)
    


  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_run_non_blocking_command(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/",
      project_name = "foo.xdc"
    )
    pv.run_command("foo_command", blocking = False)


    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn("foo_command\n", calls)
    self.assertNotIn("PYVADO_COMMAND_DONE\n", calls)

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_run_blocking_command(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/",
      project_name = "foo.xdc"
    )
    pv.run_command("foo_command", blocking = True)

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn("foo_command\n", calls)
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)
    self.assertTrue(any("PYVADO_COMMAND_DONE" in s for s in calls))

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_open_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xdc"

    pv = Pyvado(
      project_path = pj_path,
      project_name = pj_name
    )
    
    pv.open_project()

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn(f"open_project {os.path.join(os.path.abspath(pj_path), pj_name)}\n", calls)
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)
    self.assertTrue(any("PYVADO_COMMAND_DONE" in s for s in calls))

    self.assertTrue(pv.project_open())

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_close_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xdc"

    pv = Pyvado(
      project_path = pj_path,
      project_name = pj_name
    )
    
    pv.open_project()
    mock_proc.stdin.flush()
    pv.close_project()

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn(f"close_project\n", calls)
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)

    self.assertFalse(pv.project_open())

  @patch('pyvado.vivadoProcess.subprocess.Popen')
  def test_enter_exit(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xdc"

    with Pyvado(project_path = pj_path, project_name = pj_name) as pv:

      calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
      mock_proc.stdin.flush()
      self.assertIn(f"open_project {os.path.join(os.path.abspath(pj_path), pj_name)}\n", calls)
      self.assertTrue(pv.project_open())
      
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertIn(f"close_project\n", calls)
    self.assertFalse(pv.project_open())
    self.assertTrue(mock_proc.kill.called)