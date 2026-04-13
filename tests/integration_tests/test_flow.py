import unittest
from pyvado import Pyvado, PyvadoError
from os import listdir 

class IntegrationTestPyvadoFlow(unittest.TestCase):

  def test_toplevel(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")
    pv.files.add_constraint_file("./tests/integration_tests/test_files/const.xdc")

    pv.flow.set_toplevel("foo1")

    pv.tcl.run("puts [get_property top [get_filesets sources_1]]", blocking=False)
    top = pv.tcl.read()

    self.assertEqual("foo1", top.strip())

  def test_synth_flow(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.tcl.run("remove_files -fileset sources_1 *")
    pv.tcl.run("remove_files -fileset constrs_1 *")

    pv.files.add_file("./tests/integration_tests/test_files/foo1.vhd")
    pv.files.add_constraint_file("./tests/integration_tests/test_files/const.xdc")

    pv.flow.set_toplevel("foo1")

    pv.flow.reset_run(run_name="synth_1")
  
    pv.flow.synthesis()

    synth_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/synth_1")

    self.assertNotEqual(len(synth_dir), 0)

  def test_impl_after_synth_flow(self):
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

    pv.flow.synthesis()

    pv.flow.implementation()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertNotEqual(len(impl_dir), 0)

  def test_run_impl_also_run_synth(self):
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

    pv.flow.implementation()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")
    synth_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/synth_1")

    self.assertNotEqual(len(synth_dir), 0)
    self.assertNotEqual(len(impl_dir), 0)

  def test_bitstream_flow_after_impl(self):
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

    pv.flow.implementation()

    pv.flow.bitstream()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertTrue((any(f.endswith(".bit") for f in impl_dir)))

  def test_run_bitstream_also_run_impl_and_synth(self):
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

    pv.flow.bitstream()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertTrue((any(f.endswith(".bit") for f in impl_dir)))

  def test_run_all(self):
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

    pv.flow.run_all()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertTrue((any(f.endswith(".bit") for f in impl_dir)))
