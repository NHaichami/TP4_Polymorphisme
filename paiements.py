import re
from abc import ABC, abstractmethod

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
RESEAUX_AUTORISES = frozenset({"BTC", "ETH", "USDT", "LTC"})


def _luhn_valide(numero: str) -> bool:
    """Vérifie un numéro de carte avec l'algorithme de Luhn."""
    somme = 0
    for position, caractere in enumerate(reversed(numero)):
        chiffre = int(caractere)
        if position % 2 == 1:
            chiffre *= 2
            if chiffre > 9:
                chiffre -= 9
        somme += chiffre
    return somme % 10 == 0


class Paiement(ABC):
    """Paiement abstrait : possède un montant protégé et une méthode payer()."""

    def __init__(self, montant: float) -> None:
        if montant <= 0:
            raise ValueError("Le montant doit être strictement positif.")
        self._montant = float(montant)

    @property
    def montant(self) -> float:
        """Montant du paiement (lecture seule)."""
        return self._montant

    def _confirmation(self, detail: str) -> str:
        """Construit le message de confirmation commun à tous les paiements."""
        return (
            f"[{self.__class__.__name__}] "
            f"Paiement de {self._montant:.2f} € confirmé ({detail})."
        )

    @abstractmethod
    def payer(self) -> str:
        """Effectue le paiement et retourne une chaîne de confirmation."""


class CarteBancaire(Paiement):
    """Paiement par carte bancaire (numéro à 16 chiffres validé par Luhn, CVV à 3 chiffres)."""

    def __init__(self, montant: float, numero: str, cvv: str) -> None:
        super().__init__(montant)
        numero_nettoye = numero.replace(" ", "")
        if not (numero_nettoye.isdigit() and len(numero_nettoye) == 16):
            raise ValueError("Le numéro de carte doit contenir 16 chiffres.")
        if not _luhn_valide(numero_nettoye):
            raise ValueError("Numéro de carte invalide (échec de la vérification de Luhn).")
        if not (cvv.isdigit() and len(cvv) == 3):
            raise ValueError("Le CVV doit contenir 3 chiffres.")
        self._numero = numero_nettoye
        self._cvv = cvv

    def payer(self) -> str:
        return self._confirmation(f"carte **** **** **** {self._numero[-4:]}")


class PayPal(Paiement):
    """Paiement via un compte PayPal identifié par un e-mail et un token d'API."""

    def __init__(self, montant: float, email: str, token_api: str) -> None:
        super().__init__(montant)
        if not EMAIL_REGEX.match(email):
            raise ValueError("Adresse e-mail invalide.")
        if len(token_api) < 8:
            raise ValueError("Le token d'API doit contenir au moins 8 caractères.")
        self._email = email
        self._token_api = token_api

    def payer(self) -> str:
        return self._confirmation(f"compte {self._email}")


class Crypto(Paiement):
    """Paiement en cryptomonnaie via un portefeuille et un réseau (BTC, ETH...)."""

    def __init__(self, montant: float, portefeuille: str, reseau: str) -> None:
        super().__init__(montant)
        if not (portefeuille.isalnum() and len(portefeuille) >= 10):
            raise ValueError(
                "L'identifiant du portefeuille doit être alphanumérique (10 caractères minimum)."
            )
        reseau = reseau.upper()
        if reseau not in RESEAUX_AUTORISES:
            raise ValueError(
                f"Réseau non supporté : {reseau}. Réseaux acceptés : "
                f"{', '.join(sorted(RESEAUX_AUTORISES))}."
            )
        self._portefeuille = portefeuille
        self._reseau = reseau

    def payer(self) -> str:
        return self._confirmation(f"{self._reseau}, portefeuille {self._portefeuille}")


def traiter_paiements(liste: list[Paiement]) -> None:
    """Appelle payer() sur chaque paiement et affiche la confirmation (polymorphisme)."""
    for paiement in liste:
        print(paiement.payer())


def main() -> None:
    paiements: list[Paiement] = [
        CarteBancaire(50, "4111 1111 1111 1111", "123"),
        CarteBancaire(120.5, "5500000000000004", "456"),
        PayPal(75.99, "alice@example.com", "tok_abcdef123456"),
        PayPal(20, "bob@example.com", "tok_xyz987654321"),
        Crypto(300, "0xA1B2C3D4E5F6", "ETH"),
        Crypto(1500, "1A1zP1eP5QGefi2D", "BTC"),
    ]
    traiter_paiements(paiements)


if __name__ == "__main__":
    main()