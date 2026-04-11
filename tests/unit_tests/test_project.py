

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

    with self.assertRaises(PyvadoError):
      pv = Pyvado(
        project_path = ""
      )
      pv.project.open()

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_pyvado_open_when_project_name_bad_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    with self.assertRaises(ValueError):
      pv = Pyvado(
        project_path = "foo/goo.xdc"
      )

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_open_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/goo.xpr"
    pv = Pyvado(
      project_path = pj_path
    )
    
    pv.project.open()

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn(f"open_project {os.path.abspath(pj_path)}\n", calls)
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)
    self.assertTrue(any("PYVADO_COMMAND_DONE" in s for s in calls))

    self.assertTrue(pv.session.projet.is_open()())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/goo.xpr"

    pv = Pyvado(
      project_path = pj_path
    )
    
    pv.project.open()
    mock_proc.stdin.flush()
    pv.project.close()

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn(f"close_project\n", calls)
    self.assertIn("puts \"PYVADO_COMMAND_DONE\"\n", calls)

    self.assertFalse(pv.session.projet.is_open()())


  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_toplevel(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/goo.xpr"

    module_name = "boo"

    pv = Pyvado(project_path = pj_path)
    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.project.set_toplevel(module_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"set_property top {module_name} [current_fileset]\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))