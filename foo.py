
from pyvado import *

if __name__ == "__main__":

  pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

  pv.project_manager.open_project()

  # pv.flow_manager.reset_run(run_name="synth_1")

  # pv.flow_manager.run_synthesis()

  # pv.flow_manager.run_implementation()

  # pv.flow_manager.run_bitstream()

  pv.hw_manager.open_hardware()
  pv.hw_manager.connect_server()
  pv.hw_manager.open_target()
  pv.hw_manager.set_bitstream()
  pv.hw_manager.program_device()