import io
import unittest
from contextlib import redirect_stdout

from paiements import CarteBancaire, Crypto, Paiement, PayPal, traiter_paiements


class TestPayer(unittest.TestCase):
    def test_carte_contient_montant_et_type(self) -> None:
        message = CarteBancaire(50, "4111111111111111", "123").payer()
        self.assertIn("50.00", message)
        self.assertIn("CarteBancaire", message)

    def test_paypal_contient_montant_et_type(self) -> None:
        message = PayPal(75.99, "alice@example.com", "tok_abcdef123456").payer()
        self.assertIn("75.99", message)
        self.assertIn("PayPal", message)

    def test_crypto_contient_montant_et_type(self) -> None:
        message = Crypto(300, "0xA1B2C3D4E5F6", "eth").payer()
        self.assertIn("300.00", message)
        self.assertIn("Crypto", message)
        self.assertIn("ETH", message)

    def test_numero_de_carte_masque(self) -> None:
        message = CarteBancaire(10, "4111111111111111", "123").payer()
        self.assertNotIn("4111111111111111", message)
        self.assertIn("1111", message)


class TestValidations(unittest.TestCase):
    def test_paiement_est_abstrait(self) -> None:
        with self.assertRaises(TypeError):
            Paiement(10)

    def test_montant_non_positif(self) -> None:
        for montant in (0, -5):
            with self.assertRaises(ValueError):
                PayPal(montant, "alice@example.com", "tok_abcdef123456")

    def test_carte_luhn_invalide(self) -> None:
        with self.assertRaises(ValueError):
            CarteBancaire(10, "4111111111111112", "123")

    def test_carte_format_invalide(self) -> None:
        with self.assertRaises(ValueError):
            CarteBancaire(10, "1234", "123")

    def test_cvv_invalide(self) -> None:
        with self.assertRaises(ValueError):
            CarteBancaire(10, "4111111111111111", "12")

    def test_email_invalide(self) -> None:
        with self.assertRaises(ValueError):
            PayPal(10, "pas-un-email", "tok_abcdef123456")

    def test_token_trop_court(self) -> None:
        with self.assertRaises(ValueError):
            PayPal(10, "alice@example.com", "abc")

    def test_reseau_inconnu(self) -> None:
        with self.assertRaises(ValueError):
            Crypto(10, "0xA1B2C3D4E5F6", "XYZ")

    def test_portefeuille_invalide(self) -> None:
        with self.assertRaises(ValueError):
            Crypto(10, "court", "BTC")


class TestTraiterPaiements(unittest.TestCase):
    def test_affiche_une_ligne_par_paiement(self) -> None:
        paiements = [
            CarteBancaire(50, "4111111111111111", "123"),
            PayPal(20, "bob@example.com", "tok_xyz987654321"),
            Crypto(300, "0xA1B2C3D4E5F6", "ETH"),
        ]
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            traiter_paiements(paiements)
        lignes = sortie.getvalue().strip().splitlines()
        self.assertEqual(len(lignes), 3)
        self.assertEqual(lignes[0], paiements[0].payer())


if __name__ == "__main__":
    unittest.main()