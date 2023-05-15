from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Any


class DrinkType(Enum):
    HOT = "HOT"
    COLD = "COLD"
    BLENDED = "BLENDED"
    MILK_TEA = "MILK_TEA"


class Size(Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class MilkType(Enum):
    WHOLE = "WHOLE"
    ALMOND = "ALMOND"


@dataclass
class Topping:
    whip_cream: bool = True
    chocolate: Optional[int] = 0


@dataclass
class Drink:
    drink_type: DrinkType
    size: Size
    topping: Topping
    milk_type: Optional[MilkType] = None
    base_price: int = 2


class SandwichType(Enum):
    PLAIN = "PLAIN"
    EGG = "EGG"
    TURKEY = "TURKEY"


class BagelType(Enum):
    PLAIN = "PLAIN"
    BUTTER = "BUTTER"
    CHEESE = "CHEESE"


@dataclass
class Breakfast:
    sandwiches: SandwichType
    bagels: BagelType
    base_price: int = 3


def check_large_size(drink_type: str):
    return drink_type in [DrinkType.COLD.value, DrinkType.BLENDED.value]


def check_drink_logic(drink: Drink):
    if drink.size.value in [Size.L.value, Size.XL.value] and \
            drink.drink_type.value not in [DrinkType.COLD.value, DrinkType.BLENDED.value]:
        raise ValueError("Don't have L size for drink type")
    if drink.milk_type and drink.drink_type.value != DrinkType.MILK_TEA.value:
        raise ValueError("Only Milk Tea can choose milk type")
    if drink.topping.chocolate and drink.drink_type.value != DrinkType.HOT.value:
        raise ValueError("Only Hot Drink can choose chocolate pump")
    if drink.topping.chocolate > 6:
        raise ValueError("Only max chocolate pump is 6")


def calculate_drink(drink: Drink):
    check_drink_logic(drink)
    price = drink.base_price
    size_price_adjustment = {Size.S.value: 0, Size.M.value: 0.5, Size.L.value: 1, Size.XL.value: 1.5}
    drink_type_price_adjustment = {DrinkType.BLENDED.value: 1, DrinkType.HOT.value: 0, DrinkType.COLD.value: 0,
                                   DrinkType.MILK_TEA.value: 0.25}
    chocolate_pump = max(drink.topping.chocolate - 2, 0)
    topping_price_adjustment = {"whip_cream": 0.5, "chocolate": chocolate_pump * 0.5}
    milk_type_price_adjustment = {MilkType.ALMOND.value: 0.5, MilkType.WHOLE.value: 0}
    price += size_price_adjustment.get(drink.size.value)
    price += drink_type_price_adjustment.get(drink.drink_type.value)
    for key, _ in drink.topping.__annotations__.items():
        price += topping_price_adjustment.get(key)
    if drink.milk_type:
        price += milk_type_price_adjustment.get(drink.milk_type.value)
    return price


def calculate_breakfast(breakfast: Breakfast):
    sandwich_price_adjustment = {SandwichType.PLAIN.value: 0, SandwichType.EGG.value: 1, SandwichType.TURKEY.value: 1}
    bagel_price_adjustment = {BagelType.PLAIN.value: 0, BagelType.CHEESE.value: 0.5, BagelType.BUTTER.value: 0.5}
    return breakfast.base_price * 2 + sandwich_price_adjustment.get(
        breakfast.sandwiches.value) + bagel_price_adjustment.get(breakfast.bagels.value)


def calculate_price1(drink_type: DrinkType, size: Size, cream_topping: bool):
    topping = Topping(whip_cream=cream_topping)
    drink = Drink(drink_type, size, topping=topping)
    return calculate_drink(drink)


def calculate_price2(drink_type: DrinkType, size: Size, cream_topping: bool, milk_type: Optional[MilkType] = None):
    topping = Topping(whip_cream=cream_topping)
    drink = Drink(drink_type, size, topping=topping, milk_type=milk_type)
    return calculate_drink(drink)


def calculate_price3(drink_type: DrinkType, size: Size, cream_topping: bool, chocolate_pump: int,
                     milk_type: Optional[MilkType] = None):
    topping = Topping(whip_cream=cream_topping, chocolate=chocolate_pump)
    drink = Drink(drink_type, size, topping=topping, milk_type=milk_type)
    return calculate_drink(drink)


def calculate_price4(sandwich: SandwichType, bagel: BagelType):
    breakfast = Breakfast(sandwiches=sandwich, bagels=bagel)
    return calculate_breakfast(breakfast)


def calculate_price5(items: List):
    total_price = 0
    for item in items:
        if isinstance(item, Drink):
            price = calculate_drink(item)
            total_price += price
            print(item, price)
        if isinstance(item, Breakfast):
            price = calculate_breakfast(item)
            total_price += price
            print(item, price)
    return total_price + total_price * 0.0725


def format_output(output: Any):
    return f"Price: {output}$"


if __name__ == "__main__":
    print(format_output(calculate_price1(DrinkType.HOT, Size.S, True)))
    print(format_output(calculate_price2(DrinkType.MILK_TEA, Size.S, True, MilkType.ALMOND)))
    print(format_output(calculate_price3(DrinkType.HOT, Size.S, True, 3)))
    print(format_output(calculate_price4(SandwichType.EGG, BagelType.BUTTER)))
    drink1 = Drink(drink_type=DrinkType.HOT, size=Size.S, topping=Topping(chocolate=4))
    drink2 = Drink(drink_type=DrinkType.MILK_TEA, size=Size.M, topping=Topping(), milk_type=MilkType.ALMOND)
    breakfast1 = Breakfast(sandwiches=SandwichType.EGG, bagels=BagelType.BUTTER)
    print(format_output(calculate_price5([drink1, drink2, breakfast1])))
