class Category:
   def __init__(self, name):
      self.name = name
      self.ledger = []
      self.deposits = 0
      self.withdrawls = 0
   
   def get_balance(self):
      return self.deposits - self.withdrawls
   
   def check_funds(self, amount):
      return not amount > self.get_balance()
   
   def deposit(self, amount, description=""):
      self.deposits = self.deposits + amount
      self.ledger.append({
         "amount": amount,
         "description": description
      })
   
   def withdraw(self, amount, description=""):
      if not self.check_funds(amount):
         return False
      
      self.withdrawls = self.withdrawls + amount
      self.ledger.append({
         "amount": -amount,
         "description": description
      })
      return True
   
   def transfer(self, amount, other_badget):
      if not self.check_funds(amount):
         return False

      self.withdraw(amount, f"Transfer to {other_badget.name}")
      other_badget.deposit(amount, f"Transfer from {self.name}")
      return True
   
   def __str__(self):
      category_str = self.name.center(30, "*")

      for obj in self.ledger:
         desc = obj["description"]
         amount = "{:.2f}".format(obj["amount"])

         desc = desc[:23] if len(desc) > 23 else desc

         category_str = category_str + "\n" \
                        + desc.ljust(23) \
                        + str(amount).rjust(7)
      
      category_str = category_str + f"\nTotal: {self.get_balance()}"

      return category_str

def create_spend_chart(categories):
   d = {}
   total = 0

   for category in categories:
      total = total + category.withdrawls
      d[category.name] = category.withdrawls
   
   for c in d:
      d[c] = int((d[c] / total) * 100) // 10
   
   chart = "Percentage spent by category"
   for p in range(100, -10, -10):
      chart = chart + "\n" \
              + str(p).rjust(3) + "| "
      for c in d:
         mark = "o  " if p // 10 <= d[c] else "   "
         chart = chart + mark
   
   chart = chart + "\n    " + "-"*(3*len(categories)+1)
   
   for line in range(len(max(*d.keys(), key=lambda name: len(name)))):
      chart = chart + "\n     "
      for c in d:
         letter = c[line] + "  " if len(c) > line else "   "
         chart = chart + letter
   
   return chart