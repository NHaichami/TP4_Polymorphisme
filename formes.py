import math
from abc import ABC, abstractmethod


class Forme(ABC):
    """Forme géométrique abstraite : toute forme doit pouvoir calculer son aire."""

    @abstractmethod
    def aire(self) -> float:
        """Retourne l'aire de la forme."""

    def __str__(self) -> str:
        return f"{self.__class__.__name__} – aire : {self.aire():.2f}"


class Cercle(Forme):
    """Cercle défini par son rayon."""

    def __init__(self, rayon: float) -> None:
        self.rayon = rayon

    def aire(self) -> float:
        return math.pi * self.rayon ** 2


class Rectangle(Forme):
    """Rectangle défini par sa largeur et sa hauteur."""

    def __init__(self, largeur: float, hauteur: float) -> None:
        self.largeur = largeur
        self.hauteur = hauteur

    def aire(self) -> float:
        return self.largeur * self.hauteur


class Triangle(Forme):
    """Triangle défini par sa base et sa hauteur."""

    def __init__(self, base: float, hauteur: float) -> None:
        self.base = base
        self.hauteur = hauteur

    def aire(self) -> float:
        return 0.5 * self.base * self.hauteur


class Carre(Rectangle):
    """Rectangle dont les côtés sont toujours égaux.

    La contrainte est garantie en permanence : modifier la largeur
    ou la hauteur modifie automatiquement l'autre dimension.
    """

    def __init__(self, cote: float) -> None:
        super().__init__(cote, cote)

    @property
    def largeur(self) -> float:
        return self._cote

    @largeur.setter
    def largeur(self, valeur: float) -> None:
        self._cote = valeur

    @property
    def hauteur(self) -> float:
        return self._cote

    @hauteur.setter
    def hauteur(self, valeur: float) -> None:
        self._cote = valeur


class ColorMixin:
    """Mixin qui ajoute une couleur et un affichage colorisé (codes ANSI)."""

    RESET = "\033[0m"
    COULEURS = {
        "rouge": "\033[31m",
        "vert": "\033[32m",
        "jaune": "\033[33m",
        "bleu": "\033[34m",
    }

    def __init__(self, *args, couleur: str = "bleu", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if couleur not in self.COULEURS:
            raise ValueError(f"Couleur inconnue : {couleur}")
        self.couleur = couleur

    def afficher_colore(self) -> None:
        """Affiche la représentation de l'objet dans sa couleur."""
        print(f"{self.COULEURS[self.couleur]}{self}{self.RESET}")


class CercleColore(ColorMixin, Cercle):
    """Cercle avec une couleur."""


class RectangleColore(ColorMixin, Rectangle):
    """Rectangle avec une couleur."""


def main() -> None:
    formes = [
        Cercle(3),
        Rectangle(4, 5),
        Triangle(6, 2),
    ]
    for forme in formes:
        print(forme)

    print()
    print(Carre(3))

    print()
    CercleColore(3, couleur="rouge").afficher_colore()
    RectangleColore(4, 5, couleur="vert").afficher_colore()


if __name__ == "__main__":
    main()

