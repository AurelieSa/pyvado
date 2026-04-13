import unittest
from pyvado import Pyvado, PyvadoError
import os

class IntegrationTestPyvadoReport(unittest.TestCase):

  def test_list_runs(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/toplevel_test.vhd")
    pv.files.add_constraint_file("./tests/integration_tests/test_files/const.xdc")

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.set_toplevel("toplevel_test")

    synth_name = "synth_1"
    impl_name = "impl_1"

    pv.flow.synthesis(synth_name)

    pv.flow.implementation(impl_name)

    runs = pv.report.get_runs()

    self.assertIn(synth_name, runs)
    self.assertIn(impl_name, runs)

  def test_list_runs_when_no_run(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/toplevel_test.vhd")
    pv.files.add_constraint_file("./tests/integration_tests/test_files/const.xdc")

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.set_toplevel("toplevel_test")

    runs = pv.report.get_runs()

    self.assertEqual(runs, [])

  def test_report_utilization(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/toplevel_test.vhd")
    pv.files.add_constraint_file("./tests/integration_tests/test_files/const.xdc")

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.set_toplevel("toplevel_test")

    synth_name = "synth_1"
    report_name = "./tests/integration_tests/test_report/test_report_utilization.txt"

    if os.path.exists(report_name):
      os.remove(report_name)

    pv.flow.synthesis(synth_name)

    pv.report.open(synth_name)

    pv.report.utilization(report_name)

    self.assertTrue(os.path.exists(report_name))

  def test_report_power(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/toplevel_test.vhd")
    pv.files.add_constraint_file("./tests/integration_tests/test_files/const.xdc")

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.set_toplevel("toplevel_test")

    synth_name = "synth_1"
    report_name = "./tests/integration_tests/test_report/test_report_power.txt"

    if os.path.exists(report_name):
      os.remove(report_name)

    pv.flow.synthesis(synth_name)

    pv.report.open(synth_name)

    pv.report.power(report_name)

    self.assertTrue(os.path.exists(report_name))


