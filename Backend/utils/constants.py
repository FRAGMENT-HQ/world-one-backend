class ActionConstants:
    Buy = 0
    Sell = 1
    Deposit = 2
    Withdraw = 3
    Transfer = 4
    Cancel = 5
    Execute = 6

    actionChoices = (
        (Buy, "Buy"),
        (Sell, "Sell"),
        (Deposit, "Deposit"),
        (Withdraw, "Withdraw"),
        (Transfer, "Transfer"),
        (Cancel, "Cancel"),
        (Execute, "Execute"),
     )
class OrderStatusConstants:
    Pending = 0
    Completed = 1
    Cancelled = 2
    Failed = 3

    orderStatusChoices = (
        (Pending, "Pending"),
        (Completed, "Completed"),
        (Cancelled, "Cancelled"),
        (Failed, "Failed"),
    )
class CurrencyConstanata:
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    