# 1. S
# the original order class does too many things
# let's break it up into classes of 'Single Responsibility'

# 2. SO
# Code should be 'open for extension' but 'closed for modification'
# i.e. we shouldn't need to modify the original code to do that
# --> If we were to add another payment type (apple pay, bitcoin, ...) we
# would have to modify the this class, which we cannot!
# Let's use class and subclasses instead

# 3. SOL
# Liskov Substitution
# If you have objects in a program, you should be able
# to replace those objects with instances of their subtypes or subclasses
# without altering the 'correctness' of the program
# --> # let's suppose paypal works with email addresses rather than security codes
#

from abc import ABC, abstractmethod


class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass


class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code
    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address):
        self.email_address = email_address
    def pay(self, order):
        print("Processing Paypal payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"


order = Order()
order.add_item("keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
processor = PaypalPaymentProcessor("jb@email.com")
processor.pay(order)
