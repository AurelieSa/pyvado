

import unittest
from pyvado import Pyvado, PyvadoError
import shutil
from pathlib import Path

class IntegrationTestPyvadoProject(unittest.TestCase):

  # def test_open_project_wrong_path(self):

  #   pv = Pyvado(
  #     project_path = "./wrong_path/pyvado_integration_test_project.xpr"
  #   )
  #   with self.assertRaises(PyvadoError):
  #     pv.project.open()

  # def test_open_project_wrong_project_name(self):

  #   pv = Pyvado(
  #     project_path = "./wrong_project_name.xpr",
  #   )
  #   with self.assertRaises(PyvadoError):
  #     pv.project.open()

  # def test_open_project(self):

  #   pv = Pyvado(
  #     project_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
  #   )
    
  #   pv.project.open()

  #   self.assertTrue(pv.session.project.is_open())

  def test_create_project(self):

    project_path = "./tests/integration_tests"
    project_name = "project_creation_test"

    p  = Path(f"{project_path}/{project_name}")

    if p.exists():
      shutil.rmtree(f"{project_path}/{project_name}")

    pv = Pyvado()

    pv.project.create("./tests/integration_tests", "project_creation_test", board="nexys 4 ddr")

    pv.tcl.run("puts [get_property board_part [current_project]]", blocking=False)
    self.assertEqual("digilentinc.com:nexys4_ddr:part0:1.1", pv.tcl.read().strip())

    pv.tcl.run("puts [get_property part [current_project]]", blocking=False)
    self.assertEqual("xc7a100tcsg324-1", pv.tcl.read().strip())

    pv.tcl.run("puts [get_property target_language [current_project]]", blocking=False)
    self.assertEqual("VHDL", pv.tcl.read().strip())

    pv.tcl.run("puts [get_property simulator_language [current_project]]", blocking=False)
    self.assertEqual("VHDL", pv.tcl.read().strip())

    self.assertTrue(pv.session.project.is_open())

