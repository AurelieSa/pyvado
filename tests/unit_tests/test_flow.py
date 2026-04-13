
import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError
import os

class TestPyvadoResetRun(unittest.TestCase):
  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_reset_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    mock_proc.stdout.reset_mock()

    with self.assertRaises(PyvadoError):
      pv.flow.reset_run()

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_reset_when_run_name_is_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.flow.reset_run(run_name = "")

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_reset_run_default_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.reset_run()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"reset_runs synth_1" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_reset_run_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    reset_run = "run_name"

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.reset_run(run_name = reset_run)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"reset_runs {reset_run}" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_synth_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(PyvadoError):
      pv.flow.synthesis()

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_synth_when_synth_name_is_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.flow.synthesis(synth_name = "")

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_synth_when_jobs_is_less_than_one(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.flow.synthesis(num_jobs = 0)

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_synth_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.synthesis()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("launch_runs synth_1 -jobs 32" in s for s in calls))
    self.assertTrue(any("wait_on_run synth_1" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_synth_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    synth_name = "synth_name"

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.synthesis(synth_name = synth_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"launch_runs {synth_name} -jobs 32" in s for s in calls))
    self.assertTrue(any(f"wait_on_run {synth_name}" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_synth_other_jobs(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    n_jobs = 12

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.synthesis(num_jobs = n_jobs)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"launch_runs synth_1 -jobs {n_jobs}" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_impl_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    mock_proc.stdout.reset_mock()

    with self.assertRaises(PyvadoError):
      pv.flow.implementation()

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_impl_when_impl_name_is_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.flow.implementation(impl_name = "")

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_impl_when_jobs_is_less_than_one(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.flow.implementation(num_jobs = 0)

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_impl_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.implementation()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("launch_runs impl_1 -jobs 32" in s for s in calls))
    self.assertTrue(any("wait_on_run impl_1" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_impl_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    impl_name = "impl_name"

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.implementation(impl_name = impl_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"launch_runs {impl_name} -jobs 32" in s for s in calls))
    self.assertTrue(any(f"wait_on_run {impl_name}" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_impl_other_jobs(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    n_jobs = 12

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.implementation(num_jobs = n_jobs)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"launch_runs impl_1 -jobs {n_jobs}" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_bitstream_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)

    mock_proc.stdout.reset_mock()

    with self.assertRaises(PyvadoError):
      pv.flow.bitstream()

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_bitstream_when_impl_name_is_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)
    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.flow.bitstream(impl_name = "")

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_run_bitstream_when_jobs_is_less_than_one(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)
    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    with self.assertRaises(ValueError):
      pv.flow. implementation(num_jobs = 0)

    self.assertFalse(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_bitstream_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)
    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.bitstream()

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("launch_runs impl_1 -to_step write_bitstream -jobs 32" in s for s in calls))
    self.assertTrue(any("wait_on_run impl_1" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_bitstream_other_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    impl_name = "impl_name"

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)
    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.bitstream(impl_name = impl_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"launch_runs {impl_name} -to_step write_bitstream -jobs 32" in s for s in calls))
    self.assertTrue(any(f"wait_on_run {impl_name}" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_run_bitstream_other_jobs(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    n_jobs = 12

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(project_path = pj_path)
    pv.project.open()

    mock_proc.stdout.readline.reset_mock()

    pv.flow.bitstream(num_jobs = n_jobs)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"launch_runs impl_1 -to_step write_bitstream -jobs {n_jobs}" in s for s in calls))

    self.assertTrue(mock_proc.stdout.readline.called)

