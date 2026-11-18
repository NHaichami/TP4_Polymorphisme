import math
import unittest

from formes import (
    Carre,
    Cercle,
    CercleColore,
    Forme,
    Rectangle,
    Triangle,
)


class TestAires(unittest.TestCase):
    def test_cercle(self) -> None:
        self.assertAlmostEqual(Cercle(3).aire(), math.pi * 9)

    def test_rectangle(self) -> None:
        self.assertEqual(Rectangle(4, 5).aire(), 20)

    def test_triangle(self) -> None:
        self.assertEqual(Triangle(6, 2).aire(), 6)

    def test_carre(self) -> None:
        self.assertEqual(Carre(3).aire(), 9)


class TestForme(unittest.TestCase):
    def test_forme_est_abstraite(self) -> None:
        with self.assertRaises(TypeError):
            Forme()

    def test_str(self) -> None:
        self.assertEqual(str(Cercle(3)), "Cercle – aire : 28.27")
        self.assertEqual(str(Rectangle(4, 5)), "Rectangle – aire : 20.00")
        self.assertEqual(str(Triangle(6, 2)), "Triangle – aire : 6.00")


class TestCarre(unittest.TestCase):
    def test_cotes_egaux_a_la_creation(self) -> None:
        carre = Carre(4)
        self.assertEqual(carre.largeur, carre.hauteur)

    def test_cotes_restent_egaux_apres_modification(self) -> None:
        carre = Carre(4)
        carre.largeur = 7
        self.assertEqual(carre.hauteur, 7)
        self.assertEqual(carre.aire(), 49)

    def test_est_un_rectangle(self) -> None:
        self.assertIsInstance(Carre(2), Rectangle)


class TestColorMixin(unittest.TestCase):
    def test_couleur_stockee(self) -> None:
        self.assertEqual(CercleColore(1, couleur="rouge").couleur, "rouge")

    def test_couleur_inconnue(self) -> None:
        with self.assertRaises(ValueError):
            CercleColore(1, couleur="violet")

    def test_aire_inchangee(self) -> None:
        self.assertAlmostEqual(CercleColore(3).aire(), math.pi * 9)


if __name__ == "__main__":
    unittest.main()