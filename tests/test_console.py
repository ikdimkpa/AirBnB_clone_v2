#!/usr/bin/python3

"""a test module for console.py"""


import io
import unittest
from unittest.mock import patch
from unittest.mock import Mock
from uuid import uuid4
from uuid import UUID
from console import process_input as pi
from console import HBNBCommand as cc
from models import storage


class TestProcessInput(unittest.TestCase):
    """TestCase for process_input"""
    def test_empty_input(self):
        """test when empty string is supplied"""
        a = pi("")
        self.assertListEqual(a, [])

    def test_non_empty_input(self):
        """test when a string is passed"""
        a = pi("-c hello")
        b = pi("he ,he he")
        c = pi("{hello all}")
        d = pi("[hello all]")
        self.assertListEqual(a, ['-c', 'hello'])
        self.assertListEqual(b, ['he', 'he', 'he'])
        self.assertListEqual(c, ['{hello all}'])
        self.assertListEqual(d, ['[hello all]'])

    def test_no_arg_passed(self):
        """test when no argument is passed"""
        with self.assertRaises(TypeError):
            a = pi()


class TestHBNBCommand(unittest.TestCase):
    """TestCase for HBNBCommand"""
    def test_do_EOF(self):
        """test the do_EOF method"""
        with self.assertRaises(SystemExit):
            cc().do_EOF("arg")

    def test_do_quit(self):
        """test the do_quit method"""
        with self.assertRaises(SystemExit):
            cc().do_quit("arg")

    def test_default(self):
        """test the do_default method"""
        c = cc()
        a = c.default("zzz")
        b = c.default("yyy \a")
        self.assertFalse(a)
        self.assertFalse(b)

    def test_do_all(self):
        """test the do_all method"""
        out = io.StringIO
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_all("zzz")
            self.assertEqual(stdout.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_all("User")
            cout = stdout.getvalue().strip()
            self.assertTrue(cout.startswith("[") and cout.endswith("]"))

    def test_do_count(self):
        out = io.StringIO
        with self.assertRaises(TypeError):
            with patch('sys.stdout', new_callable=out) as stdout:
                cc().do_count()
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_count("User")
            cout = stdout.getvalue().strip()
            self.assertTrue(int(cout) >= 0)

    def test_do_create(self):
        out = io.StringIO
        with self.assertRaises(TypeError):
            with patch('sys.stdout', new_callable=out) as stdout:
                cc().do_create()
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_create("")
            self.assertEqual(stdout.getvalue(), "** class name missing **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_create("ZZZ")
            self.assertEqual(stdout.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_create("User")
            value = UUID(stdout.getvalue().strip(), version=4)
            self.assertTrue(value)
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_create('State name="Lagos"')
            value = UUID(stdout.getvalue().strip(), version=4)
            self.assertTrue(value)
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_create("Place number_rooms=4 latitude=37.773972")
            value = UUID(stdout.getvalue().strip(), version=4)
            self.assertTrue(value)
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_create("State name=Lagos")
            value = UUID(stdout.getvalue().strip(), version=4)
            self.assertTrue(value)

    def test_do_destroy(self):
        out = io.StringIO
        with self.assertRaises(TypeError):
            with patch('sys.stdout', new_callable=out) as stdout:
                cc().do_destroy()
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_destroy("")
            self.assertEqual(stdout.getvalue(), "** class name missing **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_destroy("ZZZ")
            self.assertEqual(stdout.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_destroy("User")
            self.assertEqual(stdout.getvalue(), "** instance id missing **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            with patch('console.storage') as storage:
                storage.all = lambda: {
                            "User.89a613f9-587b-48a4-a5f1-3138a2a23142":
                            "vanbliser"}
                cc().do_destroy("User 99a613f9-587b-48a4-a5f1-3138a2a23142")
                self.assertEqual(stdout.getvalue(),
                                 "** no instance found **\n")
        with patch('console.storage') as storage:
            storage.all = lambda: {
                        "User.89a613f9-587b-48a4-a5f1-3138a2a23142":
                        "vanbliser"}
            storage.save = Mock()
            cc().do_destroy("User 89a613f9-587b-48a4-a5f1-3138a2a23142")
            storage.save.assert_called()

    def test_do_show(self):
        out = io.StringIO
        with self.assertRaises(TypeError):
            with patch('sys.stdout', new_callable=out) as stdout:
                cc().do_show()
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_show("")
            self.assertEqual(stdout.getvalue(), "** class name missing **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_show("ZZZ")
            self.assertEqual(stdout.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            cc().do_show("User")
            self.assertEqual(stdout.getvalue(), "** instance id missing **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            with patch('console.storage') as storage:
                storage.all = lambda: {
                            "User.89a613f9-587b-48a4-a5f1-3138a2a23142":
                            "vanbliser"}
                cc().do_destroy("User 99a613f9-587b-48a4-a5f1-3138a2a23142")
                self.assertEqual(stdout.getvalue(),
                                 "** no instance found **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            with patch('console.storage') as storage:
                storage.all = lambda: {
                            "User.89a613f9-587b-48a4-a5f1-3138a2a23142":
                            "vanbliser"}
                cc().do_show("User 89a613f9-587b-48a4-a5f1-3138a2a23142")
                self.assertEqual(stdout.getvalue(), "vanbliser\n")

    def test_do_update(self):
        out = io.StringIO
        with self.assertRaises(TypeError):
            with patch('sys.stdout', new_callable=out) as stdout:
                cc().do_update()
        with patch('sys.stdout', new_callable=out) as stdout:
            a = cc().do_update("")
            self.assertEqual(stdout.getvalue(), "** class name missing **\n")
            self.assertEqual(a, None)
        with patch('sys.stdout', new_callable=out) as stdout:
            b = cc().do_update("ZZZ")
            self.assertEqual(stdout.getvalue(), "** class doesn't exist **\n")
            self.assertEqual(b, None)
        with patch('sys.stdout', new_callable=out) as stdout:
            c = cc().do_update("User")
            self.assertEqual(stdout.getvalue(), "** instance id missing **\n")
            self.assertEqual(c, None)
        with patch('sys.stdout', new_callable=out) as stdout:
            with patch('console.storage') as storage:
                storage.all = lambda: {
                            "User.89a613f9-587b-48a4-a5f1-3138a2a23142":
                            "vanbliser"}
                cc().do_update("User 99a613f9-587b-48a4-a5f1-3138a2a23142")
                self.assertEqual(stdout.getvalue(),
                                 "** no instance found **\n")
        with patch('sys.stdout', new_callable=out) as stdout:
            with patch('console.storage') as storage:
                storage.all = lambda: {
                            "User.89a613f9-587b-48a4-a5f1-3138a2a23142":
                            "vanbliser"}
                e = cc().do_update('User 89a613f9-587b-48a4-a5f1-3138a2a23142')
                err_msg = "** attribute name missing **\n"
                self.assertEqual(stdout.getvalue(), err_msg)
                self.assertEqual(e, None)
        with patch('sys.stdout', new_callable=out) as stdout:
            with patch('console.storage') as storage:
                storage.all = lambda: {
                            "User.89a613f9-587b-48a4-a5f1-3138a2a23142":
                            "vanbliser"}
                e = cc().do_update('User 89a613f9-587b-48a4-a5f1-3138a2a23142')
                err_msg = "** attribute name missing **\n"
                self.assertEqual(stdout.getvalue(), err_msg)
                self.assertEqual(e, None)


if __name__ == "__main__":
    unittest.main()
