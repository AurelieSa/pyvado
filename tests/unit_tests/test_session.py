import unittest
from unittest.mock import MagicMock, patch
from pyvado import PyvadoSession, PyvadoError
from pathlib import Path

class TestPyvadoSession(unittest.TestCase):

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_error_project_path_if_none(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    ps = PyvadoSession()

    with self.assertRaises(PyvadoError):
      ps.project_path

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_error_project_name_if_none(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    ps = PyvadoSession()

    with self.assertRaises(PyvadoError):
      ps.project_name

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_error_project_dir_if_none(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    ps = PyvadoSession()

    with self.assertRaises(PyvadoError):
      ps.project_dir

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_error_if_project_dir_is_not_xpr(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    with self.assertRaises(ValueError):
      PyvadoSession("foo.xdc")

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_project_path(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    path = "foo/bar.xpr"

    ps = PyvadoSession(path)

    path = Path(path).resolve()

    self.assertEqual(ps.project_path, path)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_project_dir(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    path = "foo/bar.xpr"

    ps = PyvadoSession(path)

    path = Path(path).resolve()

    self.assertEqual(ps.project_dir, path.parent)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_project_name(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.return_value = "PYVADO_COMMAND_DONE\n"

    path = "foo/bar.xpr"

    ps = PyvadoSession(path)

    path = Path(path).resolve()

    self.assertEqual(ps.project_name, path.stem)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_get_parts_no_filter(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "part1 part2 part3 part4\n"
    ]

    ps = PyvadoSession()

    l = ps.get_parts()

    self.assertEqual(len(l), 4)

    self.assertEqual([f"part{i}" for i in range(1, 4+1)], l)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_get_parts_correct_filter(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "p-xz-7 p-xz-8\n"
    ]

    ps = PyvadoSession()

    l = ps.get_parts(filter="p xz")

    self.assertEqual(len(l), 2)

    self.assertEqual(["p-xz-7", "p-xz-8"], l)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("*p*xz*" in c for c in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_get_parts_incorrect_filter(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "\n"
    ]

    ps = PyvadoSession()

    l = ps.get_parts(filter="foo")

    self.assertEqual(len(l), 0)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_get_boards_no_filter(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "board1 board2 board3 board4\n"
    ]

    ps = PyvadoSession()

    l = ps.get_boards()

    self.assertEqual(len(l), 4)

    self.assertEqual([f"board{i}" for i in range(1, 4+1)], l)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_get_boards_correct_filter(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "digilent:nexys-4-ddr digilent:nexys-A7-100t\n"
    ]

    ps = PyvadoSession()

    l = ps.get_parts(filter="nexys")

    self.assertEqual(len(l), 2)

    self.assertEqual(["digilent:nexys-4-ddr", "digilent:nexys-A7-100t"], l)

    calls = [c.args[0] for c in mock_proc.stdin.write.call_args_list]
    self.assertTrue(any("*nexys*" in c for c in calls))

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def test_get_boards_incorrect_filter(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "\n"
    ]

    ps = PyvadoSession()

    l = ps.get_parts(filter="foo")

    self.assertEqual(len(l), 0)

  @patch('pyvado.pyvado_process.subprocess.Popen')
  def get_version(self, mock_popen):

    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc

    mock_proc.poll.return_value = None
    mock_proc.stdout.readline.side_effect = [
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n",
      "PYVADO_COMMAND_DONE\n",
      "2025.1.2\n"
    ]

    ps = PyvadoSession()

    self.assertEqual("2025.1.2",ps.version())