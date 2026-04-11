"""
Basic exemple of how send TCL command with Pyvado
"""

from pyvado import Pyvado

if __name__ == "__main__":

  # open pyvado
  with Pyvado() as pv:
    #pyvado is open, we can send TCL directly to vivado

    # we will send a simple puts TCL command and read the output of vivado.
    # To do that use run_command with blocking=False
    pv.tcl.run(
      cmd = """puts \"Hello Pyvado\" \n""",
      blocking=False
    )

    # To read the vivado output use read_output()
    print(pv.tcl.read()) 

    # congrats! you run your first command