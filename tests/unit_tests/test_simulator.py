import unittest
from unittest.mock import MagicMock, patch
from pyvado.pyvado_process import PyvadoProcess
from pyvado.pyvado_error import PyvadoError
from pyvado import Pyvado
import os
from pathlib import Path

class TestPyvadoFileManager(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_open_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.simulator.open()

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_simulator(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.simulator.open()

    self.assertTrue(pv.session.simulator.is_open())

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("launch_simulation" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_restart_simulator_when_simulator_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.simulator.restart()

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_restart_simulator(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.simulator.open()

    mock_proc.stdin.reset_mock()

    pv.simulator.restart()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("restart" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_simulator_restart_when_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.simulator.open()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("restart" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_simulator_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.simulator.open()
    pv.simulator.close()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("close_sim" in s for s in calls))

    self.assertFalse(pv.session.simulator.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_simulator_close_do_nothing_if_simulator_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    mock_proc.stdin.reset_mock()

    pv.simulator.close()

    self.assertFalse(mock_proc.stdin.write.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertFalse(any("close_sim" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_set_toplevel_when_project_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.simulator.set_toplevel("foo.vhd")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_set_toplevel_simulator(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.simulator.open()

    pv.simulator.set_toplevel("foo")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"set_property top foo [get_filesets sim_1]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_set_toplevel_when_simulator_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.simulator.set_toplevel("foo")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"set_property top foo [get_filesets sim_1]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_when_simulator_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.simulator.run()

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_run_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    pv.simulator.open()

    pv.simulator.run()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"run all" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_if_wrong_time_unit(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.simulator.run("100m")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_if_wront_format(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.simulator.run("ns")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_open_saif_when_simulator_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.simulator.log_saif("./test/unit_tests/files/foo.saif")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_open_saif(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.simulator.open()

    saif_file = "./test/unit_tests/files/foo.saif"

    pv.simulator.log_saif(saif_file)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"open_saif {os.path.abspath(saif_file)}" in s for s in calls))
    self.assertTrue(pv.session.saif.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_log_saif_scope_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.simulator.open()

    saif_file = "./test/unit_tests/files/foo.saif"

    pv.simulator.log_saif(saif_file)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"log_saif [get_objects -r *]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_log_saif_scope_defined(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.simulator.open()

    saif_file = "./test/unit_tests/files/foo.saif"

    scope = "bar"

    pv.simulator.log_saif(saif_file, scope=scope)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"log_saif [get_objects -r /{scope}/*]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_saif(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.simulator.open()

    saif_file = "./test/unit_tests/files/foo.saif"

    pv.simulator.log_saif(saif_file)
    pv.simulator.close_saif()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"close_saif" in s for s in calls))
    self.assertFalse(pv.session.saif.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_saif_not_called_if_saif_not_open(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.simulator.open()

    mock_proc.stdin.reset_mock()

    pv.simulator.close_saif()

    self.assertFalse(mock_proc.stdin.write.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_saif_when_close_simulator(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.simulator.open()

    saif_file = "./test/unit_tests/files/foo.saif"

    pv.simulator.log_saif(saif_file)
    pv.simulator.close()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"close_saif" in s for s in calls))
    self.assertFalse(pv.session.saif.is_open())