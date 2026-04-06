import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError

class TestPyvadoProgramDevice(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_program_device_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)

    with self.assertRaises(PyvadoError):
      pv.program_device(top_module = "foo")

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_program_device_when_top_module_is_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.program_device(top_module = "")

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_program_device_when_impl_name_is_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.program_device(top_module = "module", impl_name = "")

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_program_device_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    path = f"{os.path.abspath(pj_path)}/goo.runs/impl_1/module.bit"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    pv.program_device(top_module = "module")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_hw_manager" in s for s in calls))
    self.assertTrue(any("connect_hw_server" in s for s in calls))
    self.assertTrue(any("current_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {path}" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_program_device_other_impl_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo"
    pj_name = "goo.xpr"

    impl_name = "impl_name"

    path = f"{os.path.abspath(pj_path)}/goo.runs/{impl_name}/module.bit"

    pv = Pyvado(project_path = pj_path, project_name = pj_name)
    pv.open_project()

    mock_proc.stdout.readline.reset_mock()

    pv.program_device(top_module = "module", impl_name = impl_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_hw_manager" in s for s in calls))
    self.assertTrue(any("connect_hw_server" in s for s in calls))
    self.assertTrue(any("current_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {path}" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)