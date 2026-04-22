
import unittest
from unittest.mock import MagicMock, patch
from pyvado.pyvado_process import PyvadoProcess
from pyvado.pyvado_error import PyvadoError
from pyvado import Pyvado
import os
from pathlib import Path

class TestPyvadoFileManager(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    with self.assertRaises(PyvadoError):
      pv.files.add_file("foo.vhd")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_with_invalid_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.files.add_file("./tests/unit_tests/files/foo.wrong")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_with_sim_and_synth_true(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.files.add_file("foo.ext", True, True)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_file_taht_doesnt_exist(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )
    pv.project.open()

    with self.assertRaises(PyvadoError):
      pv.files.add_file("boo.vhd", True, True)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    file_name = "./tests/unit_tests/files/bar.vhd"

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      f"{os.path.abspath(file_name)}\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.files.add_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_no_force(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    file_name = "./tests/unit_tests/files/bar.vhd"

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      f"{os.path.abspath(file_name)}\n",
      "PYVADO_COMMAND_DONE\n"
    ]

    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.files.add_file(file_name, force=False)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse  {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_synth_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    file_name = "./tests/unit_tests/files/bar.vhd"

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      f"{os.path.abspath(file_name)}\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.files.add_file(file_name, used_in_synth=True, used_in_sim=False)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation False [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_file_sim_only(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    file_name = "./tests/unit_tests/files/bar.vhd"

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      f"{os.path.abspath(file_name)}\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.files.add_file(file_name, used_in_sim=True, used_in_synth=False)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis False [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_copy_default(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/bar.vhd"

    pv.files.add_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_file_copy_no_force(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/bar.vhd"

    pv.files.add_file(file_name, force=False, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse  {os.path.abspath(file_name)}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/foo.xdc"

    pv.files.add_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_multiple_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    files = ["./tests/unit_tests/files/bar.vhd", "./tests/unit_tests/files/foo.vhd"]

    pv.files.add_file(files)

    files = ' '.join([str(Path(f).resolve()) for f in files])

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {files}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_multiple_file_if_one_does_not_exists(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    files = ["./tests/unit_tests/files/bar.vhd", "./tests/unit_tests/files/boo.vhd"]

    with self.assertRaises(PyvadoError):
      pv.files.add_file(files)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_multiple_file_if_one_has_bad_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    files = ["./tests/unit_tests/files/bar.vhd", "./tests/unit_tests/files/foo.wrong"]

    with self.assertRaises(PyvadoError):
      pv.files.add_file(files)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_multiple_file_with_seperated_constrainst(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    vhdl_file = "./tests/unit_tests/files/bar.vhd"
    xdc_file = "./tests/unit_tests/files/foo.xdc"

    pv.files.add_file([vhdl_file, xdc_file])

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(vhdl_file)}\n" in s for s in calls))
    self.assertTrue(any(f"add_files -fileset constrs_1 -norecurse -force {os.path.abspath(xdc_file)}\n" in s for s in calls))


  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_constrainst_file_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/foo.xdc"

    pv.files.add_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_simulation_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    file_name = "./tests/unit_tests/files/bar.vhd"

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      f"{os.path.abspath(file_name)}\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.files.add_simulation_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {os.path.abspath(file_name)}" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_simulation True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))
    self.assertTrue(any(f"set_property used_in_synthesis False [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_simulation_file_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/bar.vhd"

    pv.files.add_simulation_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -norecurse -force {os.path.abspath(file_name)}" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_constrainst_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    file_name = "./tests/unit_tests/files/foo.xdc"

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      "PYVADO_COMMAND_DONE\n",
      f"{os.path.abspath(file_name)}\n",
      "PYVADO_COMMAND_DONE\n"
    ]
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    

    pv.files.add_constraint_file(file_name)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_simulation True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))
    self.assertFalse(any(f"set_property used_in_synthesis True [get_files {{{os.path.abspath(file_name)}}}]" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_constrainst_file_copy(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/foo.xdc"

    pv.files.add_constraint_file(file_name, import_file=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"import_files -fileset constrs_1 -norecurse -force {os.path.abspath(file_name)}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_add_constraint_file_with_correct_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    with self.assertRaises(ValueError):
      pv.files.add_constraint_file("foo.vhd")

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
      pv.files.remove_file("foo.vhd")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_remove_file(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "foo/foo.xpr"
    file_path_if_copy = "foo/foo.srcs/sources_1/import/bar.vhd"

    pv = Pyvado(
      project_path = pj_path
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/bar.vhd"

    pv.files.remove_file(file_name)

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
    file_path_if_copy = "foo/foo.srcs/sources_1/import/bar.vhd"

    pv = Pyvado(
      project_path = pj_path
    )

    pv.project.open()

    file_name = "./tests/unit_tests/files/bar.vhd"

    mock_proc.stdout.flush()
    mock_proc.stdout.readline.side_effect = [f"{os.path.abspath(file_path_if_copy)}\n", "PYVADO_COMMAND_DONE\n"]

    pv.files.remove_file(file_name, delete_from_disk=True)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"remove_files {file_name}\n" in s for s in calls))
    self.assertTrue(any(f"update_compile_order" in s for s in calls))
    self.assertTrue(any(f"file delete -force {os.path.abspath(file_path_if_copy)}" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_cant_get_file_when_project_close(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    correct_list = [
      "/Volumes/Disque Dur/Photos",
      "/usr/local/bin",
      "/home/user/image.png"
    ]

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    mock_proc.stdout.readline.return_value = '"/Volumes/Disque Dur/Photos" /usr/local/bin /home/user/image.png\n'

    with self.assertRaises(PyvadoError):
      pv.files.get_files()

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
    pv.project.open()

    mock_proc.stdout.flush()
    mock_proc.stdout.readline.return_value = '"/Volumes/Disque Dur/Photos" /usr/local/bin /home/user/image.png\n'

    self.assertEqual(pv.files.get_files(), correct_list)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_can_add_folder(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    files = ["./tests/unit_tests/files/foo_folder/folder_file1.vhd", "./tests/unit_tests/files/foo_folder/folder_file0.vhd"]

    pv.files.add_directory("./tests/unit_tests/files/foo_folder")

    files = ' '.join([str(Path(f).resolve()) for f in files])

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {files}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_wrong_extension_files_are_ignored_when_add_dir(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.files.add_directory("./tests/unit_tests/files/bar_folder")

    files = os.path.abspath("./tests/unit_tests/files/bar_folder/folder_bar0.vhd")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {files}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_add_subdirectory(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    pv.files.add_directory("./tests/unit_tests/files/baz_folder")

    files = os.path.abspath("./tests/unit_tests/files/baz_folder/baz_subfolder/baz_file.vhd")

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any(f"add_files -norecurse -force {files}\n" in s for s in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_error_if_directory_not_exists(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado(
      project_path = "foo/foo.xpr"
    )

    pv.project.open()

    with self.assertRaises(ValueError):
      pv.files.add_directory("./tests/unit_tests/files/wrong_folder")
