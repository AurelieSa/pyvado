
import unittest
from pyvado import Pyvado, PyvadoError
import os

class IntegrationTestPyvadoSimulator(unittest.TestCase):

  def test_simulator(self):

    pv = Pyvado(
      project_path = "./wrong_path/pyvado_integration_test_project.xpr"
    )

    pv.project.open("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr")

    pv.tcl.run("remove_files [get_files]")

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    pv.simulator.set_toplevel("foo1")

  def test_open_simulator(self):

    pv = Pyvado(
      project_path = "./wrong_path/pyvado_integration_test_project.xpr"
    )

    pv.project.open("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr")

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    pv.simulator.set_toplevel("foo1")

    pv.simulator.open()
    
    self.assertTrue(pv.session.simulator.is_open())

    pv.simulator.close()

    self.assertFalse(pv.session.simulator.is_open())

  def test_log_saif(self):

    pv = Pyvado(
      project_path = "./wrong_path/pyvado_integration_test_project.xpr"
    )

    pv.project.open("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr")

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    pv.simulator.set_toplevel("foo1")

    pv.simulator.open()

    os.remove("./tests/integration_tests/test_files/foo.saif")

    pv.simulator.log_saif("./tests/integration_tests/test_files/foo.saif")

    pv.simulator.close()

    self.assertTrue(os.path.exists("./tests/integration_tests/test_files/foo.saif"))

  def test_run_simulator(self):

    pv = Pyvado(
      project_path = "./wrong_path/pyvado_integration_test_project.xpr"
    )

    pv.project.open("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr")

    pv.tcl.run("remove_files [get_files]")

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")

    pv.simulator.set_toplevel("foo1")

    pv.simulator.open()

    saif_file = "./tests/integration_tests/test_files/foo.saif"

    pv.simulator.log_saif(saif_file)

    pv.simulator.run("80ns")

    f = open(saif_file, 'r')
    self.assertIn(f.read(), "DURATION 80000")

    pv.simulator.close()