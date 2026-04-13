
import unittest
from pyvado import Pyvado, PyvadoError
import os
from pathlib import Path

class IntegrationTestPyvadoFile(unittest.TestCase):

  def test_add_file(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.tcl.run("puts [get_files]", False)

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    pv.tcl.run("puts [get_files]", False)
    files = pv.tcl.read()

    files = [f for f in files if not f.endswith(".dcp")]

    self.assertNotEqual(len(files), 1)

  def test_get_files(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    file_path = "./tests/integration_tests/test_files/foo1.vhd"

    pv.files.add_file(file_path)

    files = pv.files.get_files()

    files = [f for f in files if not f.endswith(".dcp")]

    self.assertEqual(len(files), 1)

  def test_get_files_when_no_files(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    files = pv.files.get_files()

    print(files)

    files = [f for f in files if not f.endswith(".dcp")]

    self.assertEqual(len(files), 0)

  def test_remove_file(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    size_before_add = len(pv.files.get_files())

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    self.assertNotEqual(len(pv.files.get_files()), 0)

    pv.files.remove_file("foo1.vhd")

    self.assertEqual(len(pv.files.get_files()),size_before_add)

  def test_add_file_copy(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    file_path = "./tests/integration_tests/test_files/foo1.vhd"

    final_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.srcs/sources_1/imports/test_files/foo1.vhd"

    pv.files.add_file(file_path, import_file=True)

    files = pv.files.get_files()

    self.assertIn(os.path.abspath(final_path), files)

  def test_delete_file_from_disk(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    file_path = "./tests/integration_tests/test_files/foo1.vhd"

    final_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.srcs/sources_1/imports/test_files/foo1.vhd"

    pv.files.add_file(file_path, import_file=True)

    pv.files.remove_file(file_path, delete_from_disk=True)

    self.assertFalse(os.path.exists(final_path))

  def test_add_directory(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    file_before_add = len(pv.files.get_files())

    pv.files.add_directory("./tests/integration_tests/test_files/")

    files_after_add = len(pv.files.get_files())

    file = [f for f in os.listdir("./tests/integration_tests/test_files/") if Path(f).resolve().suffix in pv.files.SUPPORTED_FILE_EXTENSIONS]

    self.assertEqual(files_after_add-file_before_add, len(file))

  def test_add_const(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    const_path = "./tests/integration_tests/test_files/const.xdc"

    pv.files.add_constraint_file(const_path)

    files = pv.files.get_files()

    self.assertIn(os.path.abspath(const_path), files)
