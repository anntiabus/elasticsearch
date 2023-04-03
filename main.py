"""
<confirmation>
    Do not modify this header, but only the checkbox mark.
    I confirm that I solved the exercises on my own, and I am able to present my solution:
    Yes [ ]    No [x]
</confirmation>
"""

def convert(amount: str) -> float:
    if amount.endswith("cl"):
        number = float(amount[:-2])
    elif amount.endswith("kg"):
        number = float(amount[:-2])
        print('Convert:', amount)
        number *= 1000
        print(number)
    elif amount.endswith("ml"):
        number = float(amount[:-2])
        print('Convert:', amount)
        number *= 0.1
        print(number)
    elif amount.endswith("l"):
        number = float(amount[:-1])
        print('Convert:', amount)
        number *= 100
        print(number)
    elif amount.endswith("g"):
        number = float(amount[:-1])
    else:
        raise ValueError(f"{amount} is not a supported unit")

    return float(number)


def get_ingredients(filepath='./ingredients.csv') -> dict[str, dict[str, str | float]]:
    ingredients = {}
    with open(filepath) as file:
        for line in file:
            line = line.replace('\n', '')
            line = line.split(',')
            unique_id = line[0]
            name = line[1]
            amount = convert(line[2])
            price = float(line[3])
            try:
                alcohol = float(line[4][:-1])
            except IndexError:
                alcohol = None
            ingredient = {
                'name': name,
                'amount': amount,
                'price': price
            }
            if alcohol:
                ingredient['alcohol'] = alcohol
            ingredients[unique_id] = ingredient
    return dict[str, dict[str, str | float]](ingredients)

def get_cocktails(filepath='./cocktails.csv') -> dict[str, dict[str, float]]:
    cocktails = {}
    with open(filepath) as file:
        for line in file:
            line = line.replace('\n', '')
            if line.startswith('# '):
                cocktail_id = line[2:]
                cocktails[cocktail_id] = {}
            elif len(line) == 0:
                pass
            else:
                amount, ingredient = line.split(',')
                amount = convert(amount)
                cocktails[cocktail_id][ingredient] = amount

    return dict[str, dict[str, float]](cocktails)


def calc_price(cocktail: dict[str, float], ingredients: dict[str, dict[str, str | float]]) -> float:
    price = 0
    for ingredient, amount in cocktail.items():
        price += ingredients[ingredient]['price'] * float(amount)
    return float(price)

def calc_volume(cocktail: dict[str, float]) -> float:
    volume = 0
    for ingredient, amount in cocktail.items():
        if ingredient not in ['Ice', 'Mint', 'Green Olive']:
            volume += amount

    return float(volume)


def calc_pure_alcohol(cocktail: dict[str, float], ingredients: dict[str, dict[str, str | float]]) -> float:
    pure_alcohol = 0
    for ingredient, amount in cocktail.items():
        if 'alcohol' in ingredients[ingredient]:
            pure_alcohol += (amount * ingredients[ingredient]['alcohol']) / 100

    return float(pure_alcohol)


def list_cocktails(cocktails, ingredients):
    for name, cocktail in cocktails.items():
        mass = calc_volume(cocktail)
        alcohol = calc_pure_alcohol(cocktail, ingredients) / mass
        price = 2*calc_price(cocktail, ingredients)
        print('{:13s} ({:.2f}) {:15.2f} Euro'.format(name, alcohol, price))


def main():
    ingredients = get_ingredients()
    cocktails = get_cocktails()
    list_cocktails(cocktails, ingredients)


if __name__ == '__main__':
    main()
