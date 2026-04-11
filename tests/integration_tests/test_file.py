
import unittest
from pyvado import Pyvado, PyvadoError
import os

class IntegrationTestPyvadoProcess(unittest.TestCase):

  def test_add_file(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("puts [get_files]", False)
    files = pv.tcl.read()
    size_before_add = len(files)

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    pv.tcl.run("puts [get_files]", False)
    files = pv.tcl.read()

    self.assertNotEqual(len(files), size_before_add)

  def test_remove_file(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("puts [get_files]", False)
    files = pv.tcl.read()
    size_before_add = len(files)

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    pv.tcl.run("puts [get_files]", False)
    files = pv.tcl.read()

    self.assertNotEqual(len(files), size_before_add)

    pv.files.remove_file("foo1.vhd")

    pv.tcl.run("puts [get_files]", False)
    files = pv.tcl.read()

    self.assertEqual(len(files),size_before_add)

  def test_get_files(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    file_path = "./tests/integration_tests/test_files/foo1.vhd"

    pv.files.add_file(file_path)

    file_path = os.path.abspath(file_path)

    files = pv.files.get_files()

    self.assertIn(file_path, files)

    pv.files.remove_file("foo1.vhd")

    files = pv.files.get_files()

    self.assertNotIn(file_path, files)

  def test_add_file_copy(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

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

    file_path = "./tests/integration_tests/test_files/foo1.vhd"

    final_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.srcs/sources_1/imports/test_files/foo1.vhd"

    pv.files.add_file(file_path, import_file=True)

    pv.files.remove_file(file_path, delete_from_disk=True)

    self.assertFalse(os.path.exists(final_path))