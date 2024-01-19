def hello(cart, discounts):
    eligible_discounts = [discount for discount in discounts if discount["condition"](cart)]
    if eligible_discounts:
        max_discount = max(eligible_discounts, key=lambda d: d["amount"])
        return max_discount["name"], max_discount["amount"]
    else:
        return "", 0


def discount(cart, discount_name, discount_amount):
    if discount_name == "tiered_50_discount":
        for product in cart:
            if product["quantity"] > 15:
                product["total_price"] *= 0.5

    return cart, discount_name, discount_amount


def main():
    products = {
        "Product A": 20,
        "Product B": 40,
        "Product C": 50,
    }

    discounts = [
        {"name": "flat_10_discount", "amount": 10, "condition": lambda cart: get_cart_total(cart) > 200},
        {"name": "bulk_5_discount", "amount": 0.05, "condition": lambda cart: any(product["quantity"] > 10 for product in cart)},
        {"name": "bulk_10_discount", "amount": 0.1, "condition": lambda cart: get_total_quantity(cart) > 20},
        {"name": "tiered_50_discount", "amount": 0, "condition": lambda cart: get_total_quantity(cart) > 30},
    ]

    cart = []

    for product_name, price in products.items():
        quantity = int(input(f"Enter quantity for {product_name}: "))
        is_gift_wrapped = input(f"Is {product_name} wrapped as a gift? (y/n): ").lower() == "y"

        total_price = price * quantity
        if is_gift_wrapped:
            total_price += quantity  

        cart.append({"product_name": product_name, "quantity": quantity, "total_price": total_price})

    subtotal = get_cart_total(cart)

    discount_name, discount_amount = hello(cart, discounts)
    cart, applied_discount, discount_amount = discount(cart, discount_name, discount_amount)

    shipping_fee = calculate_shipping_fee(cart)

    total = subtotal - discount_amount + shipping_fee

    print("\nInvoice:")
    for product in cart:
        print(f"{product['product_name']} - Quantity: {product['quantity']} - Total: ${product['total_price']}")

    print(f"\nSubtotal: ${subtotal}")
    print(f"Discount applied ({applied_discount}): -${discount_amount}")
    print(f"Shipping Fee: ${shipping_fee}")
    print(f"\nTotal: ${total}")


def get_cart_total(cart):
    return sum(product["total_price"] for product in cart)


def get_total_quantity(cart):
    return sum(product["quantity"] for product in cart)


def calculate_shipping_fee(cart):
    total_quantity = get_total_quantity(cart)
    return (total_quantity // 10) * 5


if __name__ == "__main__":
    main()

