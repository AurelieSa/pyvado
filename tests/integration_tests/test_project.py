

import unittest
from pyvado import Pyvado, PyvadoError

class IntegrationTestPyvadoOpenProject(unittest.TestCase):

  def test_open_project_wrong_path(self):

    pv = Pyvado(
      project_path = "./wrong_path/pyvado_integration_test_project.xpr"
    )
    with self.assertRaises(PyvadoError):
      pv.project.open()

  def test_open_project_wrong_project_name(self):

    pv = Pyvado(
      project_path = "./wrong_project_name.xpr",
    )
    with self.assertRaises(PyvadoError):
      pv.project.open()

  def test_open_project(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    
    pv.project.open()

    self.assertTrue(True)

  def test_set_toplevel(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.project.set_toplevel("toplevel_test")

    pv.tcl.run("puts [get_property top [current_fileset]]", False)

    self.assertEqual(pv.tcl.read(), "toplevel_test\n")

  def test_set_toplevel_wrong_topmodule_name(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.project.set_toplevel("wrong_top")

    pv.tcl.run("puts [get_property top [current_fileset]]", False)


    self.assertNotEqual(pv.tcl.read(), "wrong_top\n")