class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, other):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {other.name}')
            other.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount <= self.balance:
            return True
        else:
            return False

    def get_withdrawals_sum(self):
        return sum([it['amount'] 
                    for it in self.ledger 
                    if it['amount'] < 0])

    def __str__(self):
        output = f'{self.name:*^30}\n'
        for item in self.ledger:
            output += f'{item["description"][:23]:<23}{item["amount"]:>7.2f}\n'
        output += f'Total: {self.balance}'
        return output


def create_spend_chart(categories):
    total_spent = 0
    for category in categories:
        total_spent += category.get_withdrawals_sum()

    spent_by_category = {
        category.name: round(category.get_withdrawals_sum() / total_spent * 100)
        for category in 
        categories
    }

    return 'Percentage spent by category\n'\
            + get_bars(spent_by_category.values())\
            + f'{" " * 4}-{"---" * len(categories)}\n'\
            + get_labels(spent_by_category.keys())


def get_bars(categories_values):
    # generate strings representing bars on chart
    bars = []
    for value in categories_values:
        bar_height = int(value / 10) + 1  # bars start at 0 level thus '+ 1'
        bars.append(' ' * (11 - bar_height) + 'o' * bar_height)  # space from 100 to top of bar filled with spaces
    
    # fill chart area with labels and bars level by level from top (100%)
    output = ''
    for i in range(11):
        output += f'{100 - (i * 10):>3}| '  # label on vertical axis: 100, 90...
        for bar in bars:
            output += f'{bar[i]}  '
        output += '\n'

    return output


def get_labels(categories_names):
    max_len = max(map(lambda it: len(it), categories_names)) # length of longest name
    
    # fill gap between actual length and max_len with spaces so all strings have the same length
    categories_names = list(map(lambda it: it + ' ' * (max_len - len(it)), categories_names))
    
    # output names in vetical manner
    output = ''
    for i in range(max_len):
        output += ' ' * 5  # gap due to lables on vertical axis
        for cat_name in categories_names:
            output += f'{cat_name[i]}  '
        # don't want to jump to next line after last line
        if i != max_len-1:
            output += '\n'

    return output
