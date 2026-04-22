

import unittest
from unittest.mock import MagicMock, patch
from pyvado import Pyvado, PyvadoError
import os

class TestPyvadoOpen(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_pyvado_open_when_project_path_empty(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    with self.assertRaises(PyvadoError):
      pv = Pyvado(
        project_path = ""
      )
      pv.project.open()

    self.assertFalse(pv.session.project.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_pyvado_open_when_project_name_bad_extension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    with self.assertRaises(ValueError):
      pv = Pyvado(
        project_path = "foo/bar.xdc"
      )

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_open_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"
    pv = Pyvado(
      project_path = pj_path
    )
    
    pv.project.open()

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn(f"open_project {os.path.abspath(pj_path)}\n", calls)

    self.assertTrue(pv.session.project.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_open_project_with_other_project_name_with_wonrg_enxtension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"
    pv = Pyvado(
      project_path = pj_path
    )

    new_pj_path = "./too.xdc"
    
    with self.assertRaises(ValueError):
      pv.project.open(new_pj_path)


  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_open_project_with_other_project_name_with_wonrg_enxtension(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"
    pv = Pyvado(
      project_path = pj_path
    )

    new_pj_path = "./too.xpr"
    
    pv.project.open(new_pj_path)

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn(f"open_project {os.path.abspath(new_pj_path)}\n", calls)

    self.assertTrue(pv.session.project.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_close_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(
      project_path = pj_path
    )
    
    pv.project.open()
    mock_proc.stdin.flush()
    pv.project.close()

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertIn(f"close_project\n", calls)

    self.assertFalse(pv.session.project.is_open())

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_no_command_when_close_no_open_project(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pj_path = "./foo/bar.xpr"

    pv = Pyvado(
      project_path = pj_path
    )
    
    mock_proc.stdin.flush()
    pv.project.close()

    self.assertTrue(mock_proc.stdout.readline.called)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]

    self.assertNotIn(f"close_project\n", calls)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_create_project_when_project_path_does_not_exist(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado()

    with self.assertRaises(ValueError):
      pv.project.create("./foo", "foo")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_create_project_when_project_path_is_not_dir(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado()

    with self.assertRaises(ValueError):
      pv.project.create("./test/unit_tests/files/bar.vhd", "foo")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_create_project_when_part_and_board_are_none(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado()

    with self.assertRaises(ValueError):
      pv.project.create("./test/unit_tests/files/", "foo", part=None, board=None)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_create_project_when_part_and_board_are_not_none(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"
    mock_proc.poll.return_value = None

    pv = Pyvado()

    with self.assertRaises(ValueError):
      pv.project.create("./test/unit_tests/files/", "foo", part="part", board="board")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_create_project_when_part_and_board_are_not_none(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "digilent:nexys-4-ddr digilent:nexys-A7-100t\n"
    ]
    mock_proc.poll.return_value = None

    pv = Pyvado()
