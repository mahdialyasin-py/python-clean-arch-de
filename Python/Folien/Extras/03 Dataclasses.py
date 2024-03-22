# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] lang="de" tags=["slide"] slideshow={"slide_type": "slide"}
#
# <div style="text-align:center; font-size:200%;">
#  <b>Dataclasses</b>
# </div>
# <br/>
# <div style="text-align:center;">Dr. Matthias Hölzl</div>
# <br/>
# <!-- 03 Dataclasses.py -->
# <!-- python_courses/slides/module_200_object_orientation/topic_140_a3_dataclasses.py -->

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# - Definition von Klassen ist in Python recht einfach
# - Benötigt aber relativ viel Boilerplate-Code, um eine Klasse mit gutem Verhalten
#   zu definieren
# - Attribute sind in `__init__()` versteckt

# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# %% tags=["keep"]
p = Point(1, 2)

# %%
p

# %%
p == Point(1, 2)


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y


# %% tags=["keep"]
p = Point(1, 2)

# %% tags=["keep"]
p

# %% tags=["keep"]
p == Point(1, 2)


# %% [markdown] lang="de" tags=["slide"] slideshow={"slide_type": "slide"}
#
# ## Dataclasses
#
# - Attribute besser sichtbar
# - `__repr__()` und `__eq__()` sind vordefiniert
# - Weitere Möglichkeiten: Siehe
#   [Dokumentation](https://docs.python.org/3/library/dataclasses.html)

# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
from dataclasses import dataclass


# %%
@dataclass
class DataPoint:
    x: float
    y: float


# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
dp1 = DataPoint(2, 3)
dp1

# %%
dp2 = DataPoint(1, 1)

# %%
dp1 == dp2

# %%
dp1 is dp2

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# - Dataclasses sind vollwertige Klassen
# - Sie können Methoden enthalten
# - Attribute können Default-Werte haben
# - Sie können vererbt werden

# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
from dataclasses import field


# %% tags=["alt"]
@dataclass
class Point3D:
    x: float = field(default=0.0)
    y: float = field(default=0.0)
    z: float = 0.0  # Python >= 3.10

    def move(self, dx=0.0, dy=0.0, dz=0.0):
        self.x += dx
        self.y += dy
        self.z += dz


# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
p3d = Point3D(1.0, 2.0)
p3d

# %%
p3d.move(dy=1.0, dz=5.0)
p3d


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# - Dataclasses erzwingen, dass Default-Werte unveränderlich sind
#   - zumindest für einige Typen ...
# - Statt ein veränderliches Objekt als Default-Wert zu übergeben, kann eine
#   Funktion verwendet werden, die ein neues Objekt zurückgibt
# - Diese Art von Funktion wird "Factory-Funktion" genannt

# %% tags=["subslide", "keep"] slideshow={"slide_type": "subslide"}
class Point:
    def __init__(self, coord=[0, 0]):  # noqa
        self.coord = coord

    def __repr__(self):
        return f"Point({self.coord})"

    def move(self, dx=0, dy=0):
        self.coord[0] += dx
        self.coord[1] += dy


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
p1 = Point()
p1

# %% tags=["keep"]
p2 = Point()
p2

# %% tags=["keep"]
p1.move(1, 2)
p1

# %% tags=["keep"]
p2


# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
def list_factory():
    return []


# %%
list_factory()


# %%
list_factory

# %%
list_factory() is list_factory()

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# - Für Listen brauchen wir keine Factory-Funktion definieren
# - Der Listen-Konstruktor `list()` leistet das gleiche

# %%
list()

# %%
list

# %%
list() is list()


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
from dataclasses import dataclass, field


# %% tags=["alt"]
@dataclass
class DefaultDemo:
    items: list = field(default_factory=list)


# %%
d1 = DefaultDemo()
d2 = DefaultDemo()

# %%
d1.items.append(1234)
print(d1)
print(d2)


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Bei Python Versionen 3.10 und früher funktioniert der Test auf unveränderliche
# Defaults nur für einige Typen aus der Standardbibliothek, nicht für
# benutzerdefinierte Typen:

# %%
# @dataclass
# class BadDefault:
#     point: Point3D = Point3D(0.0, 0.0)


# %%
# bd1 = BadDefault()
# bd2 = BadDefault()
# bd1, bd2

# %%
# bd1.point.move(1.0, 2.0)
# bd1, bd2


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# # Workshop: Einkaufsliste
#
# In dieser Aufgabe wollen wir eine Einkaufsliste definieren, die geplante
# Einkäufe verwalten kann. Eine Einkaufsliste soll aus Einträgen bestehen, die
# ein Produkt und die davon benötigte Menge enthalten.
#
# Es sollen sowohl die Einkaufsliste selber als auch die Einträge durch
# benutzerdefinierte Datentypen repräsentiert werden.
#
# Falls Sie die Lösung als Python-Projekt statt als Notebook implementieren wollen,
# ist in `examples/ShoppingListStarterKit` in Projektgerüst, das Sie als
# Startpunkt hernehmen können. In `examples/ShoppingList` ist ein Lösungsvorschlag.

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Definieren Sie zunächst eine Klasse `ShoppingListItem`, die folgende Attribute hat:
# - `product: str`
# - `price: float`
# - `amount: int`
# Verwenden Sie den `@dataclass` Decorator um die Klasse zu definieren. Verwenden Sie
# einen Default-Wert von 1 für `amount`.

# %%
from dataclasses import dataclass


# %%
@dataclass
class ShoppingListItem:
    product: str
    price: float
    amount: int = 1


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
# Erzeugen sie ein `ShoppingListItem`, das 2 Pakete Kaffee zu je Eur 6.99 repräsentiert:

# %% lang="de"
ShoppingListItem("Kaffee", 6.99, 2)


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Erweitern Sie die Klasse `ShoppingListItem` um eine Methode `total_price()`,
# die den Gesamtpreis des Eintrags berechnet.

# %%
@dataclass
class ShoppingListItem:
    product: str
    price: float
    amount: int = 1

    def total_price(self):
        return self.price * self.amount


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Definieren Sie eine Variable `mein_kaffee`, die ein `ShoppingListItem`
# repräsentiert, das 2 Pakete Kaffee zu je Eur 6.99 repräsentiert:

# %% lang="de"
mein_kaffee = ShoppingListItem("Kaffee", 6.99, 2)

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Berechnen Sie den Gesamtpreis von `mein_kaffee`:

# %% lang="de"
mein_kaffee.total_price()

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Definieren Sie eine Klasse `ShoppingList`, die eine Liste von
# `ShoppingListItem`-Instanzen beinhaltet:
#
# - Verwenden Sie den `@dataclass` Decorator
# - Die Klasse hat ein Attribut `items` vom Typ `list`
#   (oder `list[ShoppingListItem]`, falls
#   Sie Python 3.9 oder neuer verwenden), das mit einer leeren Liste
#   Initialisiert wird.
# - Die Methode `add_item(self, item: ShoppingListItem)` fügt ein
#   `ShoppingListItem` zur Einkaufsliste hinzu.
# - Die Methode `total_price(self)` berechnet den Gesamtpreis der
#   Einkaufsliste.

# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
from dataclasses import field


# %%
@dataclass
class ShoppingList:
    items: list[ShoppingListItem] = field(default_factory=list)

    def add_item(self, item: ShoppingListItem):
        self.items.append(item)

    def total_price(self):
        return round(sum(item.total_price() for item in self.items), 2)


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Definieren Sie Variable `meine_einkaufsliste`, die eine Einkaufsliste mit
# folgenden ShoppingListItems repräsentiert:
#
# - 2 Pakete Tee à 1.99
# - 1 Paket Kaffee à 6.99
#

# %% lang="de"
meine_einkaufsliste = ShoppingList(
    [ShoppingListItem("Tee", 1.99, 2), ShoppingListItem("Kaffee", 6.99)]
)

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Berechnen Sie den Gesamtpreis von `meine_einkaufsliste`:

# %% lang="de"
meine_einkaufsliste.total_price()

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# - Was ist die Ausgabe von `print(meine_einkaufsliste)`?
# - Was ist die Ausgabe von `print(repr(meine_einkaufsliste))`?

# %% lang="de"
print(str(meine_einkaufsliste))
print(repr(meine_einkaufsliste))

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Erweitern Sie die Klasse `ShoppingList` um eine
# [`__str__()`-Methode](
#    https://docs.python.org/3/reference/datamodel.html#object.__str__),
# so dass:
#
# ```python
# print(meine_einkaufsliste)
# ```
#
# folgende Ausgabe erzeugt:
#
# ```
# Einkaufsliste
#   2 x Tee à 1.99 = 3.98
#   1 x Kaffee à 6.99 = 6.99
# Gesamt: 10.97
# ```
#
# *Hinweis:* Sie müssen die Definition von `meine_einkaufsliste` möglicherweise erneut
# auswerten, nachdem Sie die Klasse `ShoppingList` erweitert haben, um die Auswirkungen
# Ihrer Änderungen zu sehen.

# %% lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
TITLE_STRING = "Einkaufsliste"  # noqa
TOTAL_STRING = "Gesamt"  # noqa


# %%
@dataclass
class ShoppingList:
    items: list[ShoppingListItem] = field(default_factory=list)

    def __str__(self):
        result = f"{TITLE_STRING}\n"
        for item in self.items:
            result += (
                f"  {item.amount} x {item.product} à {item.price}"
                f" = {item.total_price()}\n"
            )
        result += f"{TOTAL_STRING}: {self.total_price()}"
        return result

    def add_item(self, item: ShoppingListItem):
        self.items.append(item)

    def total_price(self):
        return round(sum(item.total_price() for item in self.items), 2)


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Evaluieren Sie die Definition von `meine_einkaufsliste` erneut und
# Drucken Sie die Einkaufsliste aus. Entspricht die Ausgabe Ihren Erwartungen?
#
# Wie sieht die Ausgabe von `repr(meine_einkaufsliste)` aus?

# %% lang="de"
meine_einkaufsliste = ShoppingList(
    [ShoppingListItem("Tee", 1.99, 2), ShoppingListItem("Kaffee", 6.99)]
)


# %% lang="de"
print(meine_einkaufsliste)

# %% lang="de"
print(repr(meine_einkaufsliste))


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Erweitern Sie die Klasse `ShoppingList` um folgende Methoden:
#
# - [`__len__()`](https://docs.python.org/3/reference/datamodel.html#object.__len__):
#   Gibt die Anzahl der Einträge in der Einkaufsliste zurück.
# - [`__getitem__()`](
#      https://docs.python.org/3/reference/datamodel.html#object.__getitem__)
#   Ermöglicht den Zugriff auf Einträge über ihren numerischen Index.
#

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Bemerkungen
#
# - Denken Sie daran, dass Sie `meine_einkaufsliste` neu auswerten müssen.
# - Sie können von `typing.Sized` erben, um statische Typchecks für die
# `__len__()` Methode zu erleichtern. Das ist aber für das korrekte Laufzeitverhalten
# des Programms nicht notwendig.
# - Nachdem `ShoppingList` sowohl `__len__()` als auch `__getitem__()` definiert,
#   können Sie auch von `typing.Sequence` erben.

# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
@dataclass
class ShoppingList:
    items: list[ShoppingListItem] = field(default_factory=list)

    def __str__(self):
        result = f"{TITLE_STRING}\n"
        for item in self.items:
            result += (
                f"  {item.amount} x {item.product} à {item.price}"
                f" = {item.total_price()}\n"
            )
        result += f"{TOTAL_STRING}: {self.total_price()}"
        return result

    def __len__(self):
        return len(self.items)

    def __getitem__(self, n):
        return self.items[n]

    def add_item(self, item: ShoppingListItem):
        self.items.append(item)

    def total_price(self):
        return round(sum(item.total_price() for item in self.items), 2)


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Stellen Sie fest, wie lange `meine_einkaufsliste` ist und
# was ihr erstes und zweites Element sind:

# %% lang="de"
meine_einkaufsliste = ShoppingList(
    [ShoppingListItem("Tee", 1.99, 2), ShoppingListItem("Kaffee", 6.99)]
)


# %% lang="de" tags=["alt"]
print(meine_einkaufsliste)

# %% lang="de"
len(meine_einkaufsliste)

# %% lang="de"
meine_einkaufsliste[0]

# %% lang="de"
meine_einkaufsliste[1]

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Was ist der Effekt des folgenden Ausdrucks?

# %% lang="de" tags=["keep"]
for item in meine_einkaufsliste:
    print(item)


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Erweitern Sie die Definition der Klasse `ShoppingList`, so dass der Indexing
# Operator `[]` auch mit einem String aufgerufen werden kann, und eine Liste mit allen
# Shopping-List-Items zurückgibt, deren `product` mit dem String übereinstimmt, oder
# eine leere Liste, falls kein solches Item existiert.
#
# Verifizieren Sie, dass ihre neue Implementierung des Indexing Operators für Integer
# und String Argumente funktioniert.
#
# Wie bewerten Sie das neue Verhalten der Klasse? Ist es eine gute Idee, den Indexing
# Operator so zu überladen? Gibt es eine bessere Alternative?
#
# *Hinweis:* Sie können die `isinstance()` Funktion verwenden um zu überprüfen,
# ob ein Objekt ein String ist.

# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
@dataclass
class ShoppingList:
    items: list[ShoppingListItem] = field(default_factory=list)

    def __str__(self):
        result = f"{TITLE_STRING}\n"
        for item in self.items:
            result += (
                f"  {item.amount} x {item.product} à {item.price}"
                f" = {item.total_price()}\n"
            )
        result += f"{TOTAL_STRING}: {self.total_price()}"
        return result

    def __len__(self):
        return len(self.items)

    def __getitem__(self, n):
        if isinstance(n, str):
            return self.find_by_product_name(n)
        return self.items[n]

    def find_by_product_name(self, product: str):
        return [item for item in self.items if item.product == product]

    def add_item(self, item: ShoppingListItem):
        self.items.append(item)

    def total_price(self):
        return round(sum(item.total_price() for item in self.items), 2)


# %% lang="de"
meine_einkaufsliste = ShoppingList(
    [
        ShoppingListItem("Tee", 1.99, 2),
        ShoppingListItem("Kaffee", 6.99),
        ShoppingListItem("Tee", 2.99, 1),
    ]
)


# %% lang="de" tags=["subslide", "alt"] slideshow={"slide_type": "subslide"}
print(meine_einkaufsliste)

# %% lang="de" tags=["alt"]
len(meine_einkaufsliste)

# %% lang="de" tags=["alt"]
meine_einkaufsliste[0]

# %% lang="de" tags=["alt"]
meine_einkaufsliste[1]

# %% lang="de" tags=["subslide", "alt"] slideshow={"slide_type": "subslide"}
meine_einkaufsliste["Tee"]

# %% lang="de" tags=["alt"]
meine_einkaufsliste["Kaffee"]

# %% lang="de" tags=["alt"]
meine_einkaufsliste["Butter"]

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Fügen Sie 2 Stück Butter (à 1.59) und 1 Laib Brot (7.49) zur Einkaufsliste
# `meine_einkaufsliste` hinzu.

# %% lang="de"
meine_einkaufsliste.add_item(ShoppingListItem("Butter", 1.59, 2))
meine_einkaufsliste.add_item(ShoppingListItem("Brot", 7.49))
meine_einkaufsliste

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
# Drucken Sie die Einkaufsliste nochmal aus.

# %% lang="de"
print(meine_einkaufsliste)

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# Was passiert, wenn Sie `Butter` und `Brot` nochmals zur Einkaufsliste
# `meine_einkaufsliste` hinzufügen?

# %% lang="de"
meine_einkaufsliste.add_item(ShoppingListItem("Butter", 1.59, 2))
meine_einkaufsliste.add_item(ShoppingListItem("Brot", 7.49))

# %% lang="de"
print(meine_einkaufsliste)


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
# *Diskussion:* Wie könnte das Verhalten der Klasse verbessert werden?

# %% tags=["subslide"] slideshow={"slide_type": "subslide"}
@dataclass
class ShoppingList:
    items: list[ShoppingListItem] = field(default_factory=list)

    def __str__(self):
        result = f"{TITLE_STRING}\n"
        for item in self.items:
            result += (
                f"  {item.amount} x {item.product} à {item.price}"
                f" = {item.total_price()}\n"
            )
        result += f"{TOTAL_STRING}: {self.total_price()}"
        return result

    def __len__(self):
        return len(self.items)

    def __getitem__(self, n):
        if isinstance(n, str):
            return self.find_by_product_name(n)
        return self.items[n]

    def find_by_product_name(self, product: str):
        return [item for item in self.items if item.product == product]

    def add_item(self, item: ShoppingListItem):
        for existing_product in self.items:
            if (
                existing_product.product == item.product
                and existing_product.price == item.price
            ):
                existing_product.amount += item.amount
                return
        self.items.append(item)

    def total_price(self):
        return round(sum(item.total_price() for item in self.items), 2)


# %% lang="de" tags=["subslide", "alt"] slideshow={"slide_type": "subslide"}
meine_einkaufsliste = ShoppingList(
    [
        ShoppingListItem("Tee", 1.99, 2),
        ShoppingListItem("Kaffee", 6.99),
        ShoppingListItem("Tea", 2.99, 1),
    ]
)


# %% lang="de" tags=["alt"]
meine_einkaufsliste.add_item(ShoppingListItem("Tee", 1.99, 2))
meine_einkaufsliste.add_item(ShoppingListItem("Brot", 7.49))

# %% lang="de" tags=["subslide", "alt"] slideshow={"slide_type": "subslide"}
print(meine_einkaufsliste)

# %% lang="de" tags=["alt"]
meine_einkaufsliste.add_item(ShoppingListItem("Tee", 2.99, 1))
meine_einkaufsliste.add_item(ShoppingListItem("Brot", 7.49))

# %% lang="de" tags=["subslide", "alt"] slideshow={"slide_type": "subslide"}
print(meine_einkaufsliste)
