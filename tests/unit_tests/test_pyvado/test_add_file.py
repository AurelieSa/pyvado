
import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError
import os

class TestPyvadoAddFile(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    file_name = "boo.vhd"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)

    with self.assertRaises(PyvadoError):
      pv.add_file(file_name)

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_when_onlysynth_and_onlysimu(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    file_name = "boo.vhd"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.add_file(file_name, True, True)

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    file_name = "boo.vhd"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    pv.add_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse \"{os.path.abspath(file_name)}\"" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]\n" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_synth_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    file_name = "boo.vhd"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    pv.add_file(file_name, synth_only = True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse \"{os.path.abspath(file_name)}\"" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_simu_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    file_name = "boo.vhd"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    pv.add_file(file_name, simu_only = True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse \"{os.path.abspath(file_name)}\"" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_set_toplevel_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    module_name = "boo"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)

    with self.assertRaises(PyvadoError):
      pv.set_toplevel(module_name)

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_toplevel(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    module_name = "boo"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    pv.set_toplevel(module_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"set_property top {module_name} [current_fileset]\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
