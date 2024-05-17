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
    orderStatusMap = {
        Pending: "Pending",
        Completed: "Completed",
        Cancelled: "Cancelled",
        Failed: "Failed",
    }
class CurrencyConstanats:
    USD = 0
    EUR = 1
    GBP = 2
    JPY = 3
    CAD = 4
    AUD = 5
    CurrencyChoices = (
        (USD, "USD"),
        (EUR, "EUR"),
        (GBP, "GBP"),
        (JPY, "JPY"),
        (CAD, "CAD"),
        (AUD, "AUD"),
    )
class CityConstants:

    all = -1

    New_Delhi = 0

    Gurgaon = 1    

    Noida    = 2

    Kolkata    = 3

    Mumbai    = 4

    Chandigarh   = 5 

    Hyderabad  = 6  

    Vadodara    = 7

    Lucknow    = 8 

    Bangalore  = 9  

    Kochi    = 10

    Chennai   = 11 

    Ludhiana    = 12

    Jalandhar    = 13

    Amritsar    = 14

    Ahmedabad    = 15

    Trichy    = 16

    Pune    = 17

    Calicut = 18   
    
    CityChoices = (
        (New_Delhi, "New Delhi"),
        (Gurgaon, "Gurgaon"),
        (Noida, "Noida"),
        (Kolkata, "Kolkata"),
        (Mumbai, "Mumbai"),
        (Chandigarh, "Chandigarh"),
        (Hyderabad, "Hyderabad"),
        (Vadodara, "Vadodara"),
        (Lucknow, "Lucknow"),
        (Bangalore, "Bangalore"),
        (Kochi, "Kochi"),
        (Chennai, "Chennai"),
        (Ludhiana, "Ludhiana"),
        (Jalandhar, "Jalandhar"),
        (Amritsar, "Amritsar"),
        (Ahmedabad, "Ahmedabad"),
        (Trichy, "Trichy"),
        (Pune, "Pune"),
        (Calicut, "Calicut"),
        (all, "All"),
    )