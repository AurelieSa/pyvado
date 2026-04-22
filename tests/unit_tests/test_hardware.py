import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError
import os

class TestPyvadoHardwareManager(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_hardware_manager_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)

    pv.hardware.open_hardware()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_hw_manager" in s for s in calls))
    

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_hardware_manager_when_project_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.project.open()

    pv.hardware.open_hardware()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_hw_manager" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_hw_is_open_after_open_hardware(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()

    self.assertTrue(pv.session.hardware.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_hw_is_close_after_close_hardware(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.close_hardware()

    self.assertFalse(pv.session.hardware.is_open())

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("close_hw_manager" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_no_command_send_if_hw_is_already_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    
    pv.hardware.close_hardware()

    self.assertFalse(pv.session.hardware.is_open())

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("close_hw_manager" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_connect_server_if_hardware_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)

    with self.assertRaises(PyvadoError):
      pv.hardware.connect_server()

    self.assertFalse(pv.session.hw_server.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_connect_server(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()

    pv.hardware.connect_server()

    self.assertTrue(pv.session.hw_server.is_open())
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("connect_hw_server" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_connect_server_with_other_url(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()

    pv.hardware.connect_server(url = "foo")

    self.assertTrue(pv.session.hw_server.is_open())
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("connect_hw_server -url foo" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_disconnect_server(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()

    pv.hardware.connect_server()
    pv.hardware.disconnect_server()

    self.assertFalse(pv.session.hw_server.is_open())
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("disconnect_hw_server" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_disconnect_server_not_call_if_server_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()

    pv.hardware.disconnect_server()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("disconnect_server" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_open_target_if_server_is_not_connected(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()

    with self.assertRaises(PyvadoError):
      pv.hardware.open_target()

    self.assertFalse(pv.session.target.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_target_after_hw_server_is_connected(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()

    pv.hardware.open_target()

    self.assertTrue(pv.session.target.is_open())
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_hw_target" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_close_target_after_open_it(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()

    pv.hardware.open_target()
    pv.hardware.close_target()

    self.assertFalse(pv.session.target.is_open())
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("close_hw_target" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_no_command_send_if_target_is_already_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)

    pv.hardware.close_target()

    self.assertFalse(pv.session.target.is_open())
    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("close_hw_target" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_bitstream_fail_if_hw_is_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()

    with self.assertRaises(PyvadoError):
      pv.hardware.set_bitstream("foo.bit")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_bitstream_fail_if_wrong_format(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    with self.assertRaises(ValueError):
      pv.hardware.set_bitstream("foo.bar")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_bitstream_fail_if_file_does_not_exists(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    with self.assertRaises(PyvadoError):
      pv.hardware.set_bitstream("foo.bit")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_bitstream(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    pv.hardware.set_bitstream(bitstream_file)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_program_device_fail_if_target_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"


    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    
    with self.assertRaises(PyvadoError):
      pv.hardware.program_device()

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_program_device(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"


    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    pv.hardware.program_device()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_bitstream_auto_detect_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    with self.assertRaises(PyvadoError):
      pv.hardware.set_bitstream()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_bitstream_auto_detect_project_open_no_bitstream(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "./tests/unit_tests",
      "PYVADO_COMMAND_DONE\n",
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.project.open()
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    with self.assertRaises(PyvadoError):
      pv.hardware.set_bitstream()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_set_bitstream_auto_detect_project_open_with_bitstream(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "./tests/unit_tests/files",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.project.open()
    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    pv.hardware.set_bitstream()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_deploy_call_every_function(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "./tests/unit_tests/files",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.project.open()
    
    pv.hardware.deploy()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_hw_manager" in s for s in calls))
    self.assertTrue(any("connect_hw_server" in s for s in calls))
    self.assertTrue(any("open_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_deploy_call_every_function_with_bard_parameters(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "./tests/unit_tests/files",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo2.bit"

    pv = Pyvado(pj_path)
    pv.project.open()
    
    pv.hardware.deploy(bitstream_path=bitstream_file, server_url="bar")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_hw_manager" in s for s in calls))
    self.assertTrue(any("connect_hw_server -url bar" in s for s in calls))
    self.assertTrue(any("open_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))
  
  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_deploy_dont_reopen_hardware_if_already_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "./tests/unit_tests/files",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.project.open()
    pv.hardware.open_hardware()

    mock_proc.stdin.write.reset_mock()
    
    pv.hardware.deploy()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("open_hw_manager" in s for s in calls))
    self.assertTrue(any("connect_hw_server" in s for s in calls))
    self.assertTrue(any("open_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_deploy_dont_reconnect_server_if_already_connected(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "./tests/unit_tests/files",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.project.open()
    pv.hardware.open_hardware()
    pv.hardware.connect_server()

    mock_proc.stdin.write.reset_mock()
    
    pv.hardware.deploy()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("open_hw_manager" in s for s in calls))
    self.assertFalse(any("connect_hw_server" in s for s in calls))
    self.assertTrue(any("open_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_deploy_dont_reopen_target_if_already_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "./tests/unit_tests/files",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.project.open()

    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()

    mock_proc.stdin.write.reset_mock()
    
    pv.hardware.deploy()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("open_hw_manager" in s for s in calls))
    self.assertFalse(any("connect_hw_server" in s for s in calls))
    self.assertFalse(any("open_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file)}}} [current_hw_device]" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_deploy_reset_bitstream_if_already_set(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n", 
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pj_path = "foo/bar.xpr"

    bitstream_file1 = "./tests/unit_tests/files/foo.bit"
    bitstream_file2 = "./tests/unit_tests/files/foo.bit"

    pv = Pyvado(pj_path)
    pv.project.open()

    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()
    pv.hardware.set_bitstream(bitstream_file1)

    mock_proc.stdin.write.reset_mock()
    
    pv.hardware.deploy(bitstream_file2)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("open_hw_manager" in s for s in calls))
    self.assertFalse(any("connect_hw_server" in s for s in calls))
    self.assertFalse(any("open_hw_target" in s for s in calls))
    self.assertTrue(any(f"set_property PROGRAM.FILE {{{os.path.abspath(bitstream_file2)}}} [current_hw_device]" in s for s in calls))
    self.assertTrue(any("program_hw_devices [current_hw_device]" in s for s in calls))