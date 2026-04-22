
import unittest
from pyvado import Pyvado, PyvadoError
import os

class IntegrationTestPyvadoSession(unittest.TestCase):

  def test_get_part(self):

    ps = Pyvado()

    parts = ps.session.get_parts()

    self.assertNotEqual(len(parts), 0)

  def test_get_part_correct_filter(self):

    ps = Pyvado()

    parts = ps.session.get_parts("xc7k70tfbv676")

    self.assertEqual(len(parts), 4)

  def test_get_part_incorrect_filter(self):

    ps = Pyvado()

    parts = ps.session.get_parts("foo")

    self.assertEqual(len(parts), 0)

  def test_get_board(self):

    ps = Pyvado()

    boards = ps.session.get_boards()

    self.assertNotEqual(len(boards), 0)

  def test_get_board_correct_filter(self):

    ps = Pyvado()

    ps.session.process.send("set_param board.repoPaths [get_param board.repoPaths]")

    boards = ps.session.get_boards("nexys")

    self.assertEqual(len(boards), 2)
    

  def test_get_board_incorrect_filter(self):

    ps = Pyvado()

    boards = ps.session.get_boards("foo")

    self.assertEqual(len(boards), 0)

  def test_get_version(self):

    pv = Pyvado()

    self.assertEqual("2025.2.1", pv.session.version())