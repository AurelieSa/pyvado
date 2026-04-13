

import unittest
from pyvado import Pyvado, PyvadoError

class IntegrationTestPyvadoProject(unittest.TestCase):

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

    self.assertTrue(pv.session.project.is_open())
