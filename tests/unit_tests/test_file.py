
import unittest
from unittest.mock import MagicMock, patch
from pyvado.pyvado_process import PyvadoProcess
from pyvado.pyvado_error import PyvadoError
from pyvado import Pyvado
import os

class TestPyvadoFileManager(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.file_manager.add_file("foo.vhd")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_with_invalid_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.file_manager.add_file("foo.ext")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_with_sim_and_synth_true(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(ValueError):
      pv.file_manager.add_file("foo.ext", True, True)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_no_force(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name, force=False)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_synth_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name, synth_only=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_sim_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name, sim_only=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_copy_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_copy_no_force(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name, force=False, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_copy_synth_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name, synth_only=True, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_copy_sim_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_file(file_name, sim_only=True, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file_sim(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_file(file_name, sim_only=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file_sim(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_file(file_name, synth_only=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file_sim_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_file(file_name, sim_only=True, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file_synth_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_file(file_name, synth_only=True, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_simulation_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_simulation_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_simulation_file_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.add_simulation_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse -force {os.path.abspath(file_name)}" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_constrainst_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_constraint_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_constrainst_file_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    file_name = "goo.xdc"

    pv.file_manager.add_constraint_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation false [get_files {os.path.abspath(file_name)}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis false [get_files {os.path.abspath(file_name)}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_constraint_file_with_correct_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project_manager.open_project()

    with self.assertRaises(ValueError):
      pv.file_manager.add_constraint_file("foo.vhd")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_remove_file_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.file_manager.remove_file("foo.vhd")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_remove_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "foo/foo.xpr"
    file_path_if_copy = "foo/foo.srcs/sources_1/import/goo.vhd"

    pv = Pyvado(
      project_path = pj_path
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    pv.file_manager.remove_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"remove_files {file_name}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertFalse(any(f"file delete -force {os.path.abspath(file_path_if_copy)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_delete_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "foo/foo.xpr"
    file_path_if_copy = "foo/foo.srcs/sources_1/import/goo.vhd"

    pv = Pyvado(
      project_path = pj_path
    )

    pv.project_manager.open_project()

    file_name = "goo.vhd"

    mock_proc.stdout.flush()
    mock_proc.stdout.readline.side_effect = [f"{os.path.abspath(file_path_if_copy)}\n", "PYVADO_COMMAND_DONE\n"]

    pv.file_manager.remove_file(file_name, delete_from_disk=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"remove_files {file_name}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"file delete -force {os.path.abspath(file_path_if_copy)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_get_file_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = '"/Volumes/Disque Dur/Photos" /usr/local/bin /home/user/image.png\n'
    mock_proc.poll.return_value = None

    correct_list = [
      "/Volumes/Disque Dur/Photos",
      "/usr/local/bin",
      "/home/user/image.png"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.file_manager.get_files()

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_get_file_correctly_parse(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = 'PYVADO_COMMAND_DONE\n'
    mock_proc.poll.return_value = None

    correct_list = [
      "/Volumes/Disque Dur/Photos",
      "/usr/local/bin",
      "/home/user/image.png"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project_manager.open_project()

    mock_proc.stdout.flush()
    mock_proc.stdout.readline.return_value = '"/Volumes/Disque Dur/Photos" /usr/local/bin /home/user/image.png\n'

    self.assertEqual(pv.file_manager.get_files(), correct_list)


