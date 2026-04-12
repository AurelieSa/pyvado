import unittest
from pyvado import PyvadoSession, PyvadoError
from pathlib import Path

class TestPyvadoSession(unittest.TestCase):

  def test_error_project_path_if_none(self):

    ps = PyvadoSession()

    with self.assertRaises(PyvadoError):
      ps.project_path

  def test_error_project_name_if_none(self):

    ps = PyvadoSession()

    with self.assertRaises(PyvadoError):
      ps.project_name

  def test_error_project_dir_if_none(self):

    ps = PyvadoSession()

    with self.assertRaises(PyvadoError):
      ps.project_dir

  def test_error_if_project_dir_is_not_xpr(self):

    with self.assertRaises(ValueError):
      PyvadoSession("foo.xdc")

  def test_project_path(self):

    path = "foo/bar.xpr"

    ps = PyvadoSession(path)

    path = Path(path).resolve()

    self.assertEqual(ps.project_path, path)

  def test_project_dir(self):

    path = "foo/bar.xpr"

    ps = PyvadoSession(path)

    path = Path(path).resolve()

    self.assertEqual(ps.project_dir, path.parent)

  def test_project_name(self):

    path = "foo/bar.xpr"

    ps = PyvadoSession(path)

    path = Path(path).resolve()

    self.assertEqual(ps.project_name, path.stem)