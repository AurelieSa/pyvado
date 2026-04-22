import unittest
from unittest.mock import MagicMock, patch
from pyvado.pyvado_process import PyvadoProcess
from pyvado.pyvado_error import PyvadoError
from pyvado import Pyvado
import os
from pathlib import Path

class TestPyvadoFileManager(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_get_runs_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.report.get_runs()

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_get_runs(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    runs = pv.report.get_runs()

    self.assertIn("synth_1", runs)
    self.assertIn("impl_1", runs)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_get_runs_when_no_runs_launch(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "Not started\n",
      "PYVADO_COMMAND_DONE\n",
      "Not started\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    runs = pv.report.get_runs()

    self.assertEqual(runs, [])

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_open_run_when_porject_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "Not started\n",
      "PYVADO_COMMAND_DONE\n",
      "Not started\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.open("impl_1")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_open_run_if_not_in_runs(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.report.open("foo")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("open_run foo" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_run(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("open_run impl_1" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_run(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.close()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("close_design" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_dont_send_command_if_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.close()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("close_design" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_utilization_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.utilization("uti.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_utilization_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.utilization("uti.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_utilization_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.utilization()

    default_file = "./utilization_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_utilization  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_utilization_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_utilization_report.txt"

    pv.report.utilization(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_utilization  -file {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_power_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.power("power.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_power_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.power("power.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_power_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.power()

    default_file = "./power_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_power  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_power_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_power_report.txt"

    pv.report.power(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_power  -file {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_set_activity_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.set_activity("./tests/unit_tests/files/foo.saif")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_set_activity_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.set_activity("./tests/unit_tests/files/foo.saif")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_saif(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    pv.report.open("impl_1")

    file_name = "./tests/unit_tests/files/foo.saif"
    
    pv.report.set_activity(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"read_saif {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_open_saif_if_wrong_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    pv.report.open("impl_1")

    file_name = "./tests/unit_tests/files/foo.vhd"
    
    with self.assertRaises(ValueError):
      pv.report.set_activity(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any(f"read_saif {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_open_when_file_does_not_exist(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    pv.report.open("impl_1")

    file_name = "./tests/unit_tests/files/buz.saif"
    
    with self.assertRaises(ValueError):
      pv.report.set_activity(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any(f"read_saif {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_saif_strip_path(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    pv.report.open("impl_1")

    file_name = "./tests/unit_tests/files/foo.saif"
    strip = "strip_path"
    
    pv.report.set_activity(file_name, strip_path=strip)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"read_saif -strip_path {strip} {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_clock_network_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.clock_network("clock_net.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_clock_network_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.clock_network("clock_network.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_clock_network_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.clock_network()

    default_file = "./clock_network_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_clock_network  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_clock_network_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_clock_network_report.txt"

    pv.report.clock_network(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_clock_network  -file {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_timing_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.timing("timing.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_timing_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.timing("timing.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_timing_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.timing()

    default_file = "./timing_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_timing_summary  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_timing_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_timing_report.txt"

    pv.report.timing(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_timing_summary  -file {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_clock_interaction_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.clock_interaction("clock_interaction.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_clock_interaction_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.clock_interaction("clock_interaction.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_clock_interaction_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.clock_interaction()

    default_file = "./clock_interaction_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_clock_interaction  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_clock_interaction_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_clock_interaction_report.txt"

    pv.report.clock_interaction(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_clock_interaction  -file {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_methodology_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.methodology("methodology.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_methodology_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.methodology("methodology.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_methodology_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.methodology()

    default_file = "./methodology_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_methodology  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_methodology_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_methodology_report.txt"

    pv.report.methodology(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_methodology  -file {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_drc_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.drc("drc.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_drc_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.drc("drc.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_drc_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.drc()

    default_file = "./drc_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_drc  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_drc_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_drc_report.txt"

    pv.report.drc(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_drc  -file {os.path.abspath(file_name)}" in s for s in calls))

  
  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_noise_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.noise("noise.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_noise_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.noise("noise.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_noise_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.noise()

    default_file = "./noise_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_ssn  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_noise_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_noise_report.txt"

    pv.report.noise(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_ssn  -file {os.path.abspath(file_name)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_operating_conditions_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    
    with self.assertRaises(PyvadoError):
      pv.report.operating_conditions("operating_conditions.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_report_operating_conditions_when_run_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()
    
    with self.assertRaises(PyvadoError):
      pv.report.operating_conditions("operating_conditions.txt")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_operating_conditions_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    pv.report.operating_conditions()

    default_file = "./operating_conditions_report.txt"

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_operating_conditions  -file {os.path.abspath(default_file)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_report_operating_conditions_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "synth_1 impl_1\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "complete\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.report.open("impl_1")

    file_name = "./foo_operating_conditions_report.txt"

    pv.report.operating_conditions(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"report_operating_conditions  -file {os.path.abspath(file_name)}" in s for s in calls))