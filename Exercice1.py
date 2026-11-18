from typing import Protocol


class Parlant(Protocol):
    """Tout objet possédant une méthode parler() retournant une chaîne."""

    def parler(self) -> str: ...


class Animal:
    """Classe de base abstraite pour les animaux."""

    def parler(self) -> str:
        """Retourne le cri de l'animal. Doit être redéfinie par les sous-classes."""
        raise NotImplementedError("Cette méthode doit être redéfinie")


class Chien(Animal):
    """Animal qui aboie."""

    def parler(self) -> str:
        return "Ouaf !"


class Chat(Animal):
    """Animal qui miaule."""

    def parler(self) -> str:
        return "Miaou !"


class Vache(Animal):
    """Animal qui meugle."""

    def parler(self) -> str:
        return "Meuh !"


class Robot:
    """Machine qui n'hérite pas d'Animal mais possède aussi parler() (duck typing)."""

    def parler(self) -> str:
        return "Bip bip !"


def faire_parler(animal: Parlant) -> None:
    """Affiche ce que dit l'objet donné, sans connaître son type."""
    print(animal.parler())


def main() -> None:
    # Collection hétérogène : on ignore le type exact de chaque élément.
    parlants: list[Parlant] = [Chien(), Chat(), Vache(), Chien(), Robot()]
    for parlant in parlants:
        faire_parler(parlant)


if __name__ == "__main__":
    main()