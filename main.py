class Category:
	def __init__(self, name):
		self.name = name
		self.ledger = []
	
	def deposit(self, amount, description = ''):
		self.ledger.append({
			'amount': amount, 
			'description': description
		})

	def withdraw(self, amount, description = ''):
		if self.check_funds(amount):
			self.ledger.append({
				'amount': -amount, 
				'description': description
			})
			return True
		
		return False

	def get_balance(self):
		return sum(item['amount'] for item in self.ledger)

	def check_funds(self, amount):
		return self.get_balance() >= amount

	def transfer(self, amount, destination):
		if self.check_funds(amount):
			self.withdraw(amount, f'Transfer to {destination.name}')
			destination.deposit(amount, f'Transfer from {self.name}')
			return True

		return False

	def __str__(self):
		output = f'{self.name:*^30}\n'

		for item in self.ledger:
			description = item['description'][:23]
			amount = f'{item["amount"]:.2f}'
			output += f'{description:<23}{amount:>7}\n'

		output += f'Total: {self.get_balance():.2f}'

		return output

def create_spend_chart(categories):
	total_spent = 0
	spent_per_category = []

	for category in categories:
		spent = 0

		for item in category.ledger:
			if item['amount'] < 0:
				spent += -item['amount']

		spent_per_category.append(spent)
		total_spent += spent
    
	percentages = [(spent / total_spent) * 100 for spent in spent_per_category]

	output = 'Percentage spent by category\n'

	for i in range(100, -1, -10):
		output += f'{i:>3}|'
		output += ''.join(' o ' if percentage >= i else '   ' for percentage in percentages)
		output += ' \n'

	output += '    ' + '-' * (3 * len(categories)) + '-\n'

	max_length = max(len(category.name) for category in categories)
	category_names = [f'{category.name:<{max_length}}' for category in categories]
	for i in range(max_length):
		output += '     '
		output += ''.join(f'{name[i]}  ' for name in category_names)
		output += '\n'

	return output.rstrip('\n')


# =========================
# Example usage
# =========================
entertainment = Category('Entertainment')
entertainment.deposit(800, 'initial deposit')
entertainment.withdraw(120, 'concert tickets')
entertainment.withdraw(45.50, 'cinema and snacks')

groceries = Category('Groceries')
groceries.deposit(600, 'initial deposit')
groceries.withdraw(85.20, 'weekly shopping')
groceries.withdraw(40, 'extra groceries')

utilities = Category('Utilities')
utilities.deposit(400, 'initial deposit')
utilities.withdraw(100, 'electricity bill')
utilities.withdraw(60, 'internet bill')

travel = Category('Travel')
travel.deposit(1000, 'initial deposit')
travel.withdraw(300, 'flight tickets')
travel.withdraw(150, 'hotel booking')

# Transfer
entertainment.transfer(50, travel)

# Category details
print(entertainment)
print(groceries)
print(utilities)
print(travel)

# Spend chart
print(create_spend_chart([entertainment, groceries, utilities, travel]))
