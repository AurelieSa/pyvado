

import unittest
from pyvado import Pyvado, PyvadoError

class IntegrationTestPyvadoOpenProject(unittest.TestCase):

  def test_open_project_wrong_path(self):

    pv = Pyvado(
      project_path = "./wrong_path/pyvado_integration_test_project.xpr"
    )
    with self.assertRaises(PyvadoError):
      pv.project_manager.open_project()

  def test_open_project_wrong_project_name(self):

    pv = Pyvado(
      project_path = "./wrong_project_name.xpr",
    )
    with self.assertRaises(PyvadoError):
      pv.project_manager.open_project()

  def test_open_project(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    
    pv.project_manager.open_project()

    self.assertTrue(True)

  def test_set_toplevel(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project_manager.open_project()

    pv.project_manager.set_toplevel("toplevel_test")

    pv.run_command("puts [get_property top [current_fileset]]", False)

    self.assertEqual(pv.read_output(), "toplevel_test\n")

  def test_set_toplevel_wrong_topmodule_name(self):

    pv = Pyvado(
      project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project_manager.open_project()

    pv.project_manager.set_toplevel("wrong_top")

    pv.run_command("puts [get_property top [current_fileset]]", False)


    self.assertNotEqual(pv.read_output(), "wrong_top\n")