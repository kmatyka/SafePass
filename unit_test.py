import unittest
from unittest.mock import patch, mock_open
from app import generate_password, code_password, recode_password, save_to_file, check_strong_password

class TestSafePass(unittest.TestCase):

    def test_generate_password(self):
        # Testy generowania haseł z różnymi parametrami
        self.assertEqual(len(generate_password('8', 1, 1, 1)), 8)
        self.assertTrue(any(char.isdigit() for char in generate_password('8', 0, 1, 0)))
        self.assertTrue(any(char.isupper() for char in generate_password('8', 1, 0, 0)))

    def test_code_password(self):
        # Testy szyfrowania hasła
        self.assertEqual(code_password("abc123!"), ")(*srqj")
        self.assertEqual(code_password("Password123"), "E)11X52&srq")

    def test_recode_password(self):
        # Testy odszyfrowywania hasła
        self.assertEqual(recode_password(")(*srqj"), "abc123!")
        self.assertEqual(recode_password("E)11X52&srq"), "Password123")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_file(self, mock_file):
        # Testy zapisywania do pliku
        save_to_file("Password123!", "MyPassword", "test_file.txt")
        mock_file.assert_called_with("test_file.txt", "a")
        mock_file().write.assert_called_once_with("MyPassword Password123!\n")

    def test_check_strong_password(self):
        # Testy sprawdzania siły hasła
        self.assertEqual(check_strong_password("aA1!"), "Słabe hasło - Hasło musi mieć co najmniej 8 znaków.")
        self.assertEqual(check_strong_password("abcd1234"), "Średnie hasło")
        self.assertEqual(check_strong_password("Abcd123!"), "Silne hasło")
        self.assertEqual(check_strong_password("short"), "Słabe hasło - Hasło musi mieć co najmniej 8 znaków.")

    

if __name__ == "__main__":
    unittest.main()
