

import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError
import os

class TestPyvadoOpen(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_pyvado_open_when_project_path_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    with self.assertRaises(ValueError):
      pv = Pyvado(
        project_path = "",
        project_name = "goo.xpr"
      )

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_pyvado_open_when_project_name_bad_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    with self.assertRaises(ValueError):
      pv = Pyvado(
        project_path = "foo",
        project_name = "goo.xdc"
      )

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_open_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

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

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

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

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_enter_exit(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    with Pyvado(project_path = pj_path, project_name = pj_name) as pv:

      calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
      mock_proc.stdin.flush()
      self.assertIn(f"open_project {os.path.join(os.path.abspath(pj_path), pj_name)}\n", calls)
      self.assertTrue(pv.project_open())
      
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertIn(f"close_project\n", calls)
    self.assertFalse(pv.project_open())
    self.assertTrue(mock_proc.kill.called)