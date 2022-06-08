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
# --> let's suppose paypal works with email addresses rather than security codes

# 4. SOLI
# Interface Segregation
# Several specific interfaces are better than one general purpose interface
# --> let's say we now have 2FA in the PaymentProcessor class
#     but the Credit processor doesn't have 2FA
#     (not all subclasses support 2FA)
#     --> better to create separate interfaces

# 4. SOLI - part2
# You can also use 'Composition' - which makes more sense in this example

# 5. SOLID
# Dependency inversion means classes should depend on abstractions, not on concrete subclasses
# Our payment processor are depending on specific authorizers
# Let's create an abstract authorizer class to pay to the Payment Processors
# Let's create another auth method: checking you are not a robot

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

class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass


class SMSAuth(Authorizer):
    authorized = False
    def verify_code(self, code):
        print(f"Verifying code {code}")
        self.authorized = True
    
    def is_authorized(self) -> bool:
        return self.authorized


class NotARobot(Authorizer):
    authorized = False
    def not_a_robot(self):
        print("Are you a robot? Nope.")
        self.authorized = True
    
    def is_authorized(self) -> bool:
        return self.authorized


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass


class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizer: Authorizer):
        self.authorizer = authorizer
        self.security_code = security_code

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
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
    def __init__(self, email_address, authorizer: Authorizer):
        self.authorizer = authorizer
        self.email_address = email_address

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing Paypal payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"


order = Order()
order.add_item("keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
authorizer = NotARobot()
processor = PaypalPaymentProcessor("jb@email.com", authorizer)
authorizer.not_a_robot()
processor.pay(order)
