from money import Money


class Transaction:
    def __init__(self):
        self.payment_identifier = None
        self.description = None
        self.amount = Money(0, currency='USD')
        self.transaction_date = None
        self.category = 'unspecified'

    def digest_string(self):
        return '{} {} {} {} category: {}'.format(self.payment_identifier, self.description, self.amount,
                                                 self.transaction_date, self.category)

    def __lt__(self, other):
        if self.transaction_date != other.transaction_date:
            return self.transaction_date < other.transaction_date
        if self.description != other.description:
            return self.description < other.description
        if self.amount != other.amount:
            return self.amount < other.amount

    def __hash__(self) -> int:
        return hash(self.payment_identifier, self.description, self.amount, self.transaction_date)

    def __eq__(self, other):
        if self.payment_identifier != other.payment_identifier:
            return False
        if self.description != other.description:
            return False
        if self.amount != other.amount:
            return False
        if self.transaction_date != other.transaction_date:
            return False

        return True
