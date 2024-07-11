class ActionConstants:
    Buy = 0
    Sell = 1

    actionChoices = (
        (Buy, "Buy"),
        (Sell, "Sell"),

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

    all = "all"
    New_Delhi = "New Delhi"
    Gurgaon = "Gurgaon"
    Noida = "Noida"
    Kolkata = "Kolkata"
    Mumbai = "Mumbai"
    Chandigarh = "Chandigarh"
    Hyderabad = "Hyderabad"
    Vadodara = "Vadodara"
    Lucknow = "Lucknow"
    Bangalore = "Bangalore"
    Kochi = "Kochi"
    Chennai = "Chennai"
    Ludhiana = "Ludhiana"
    Jalandhar = "Jalandhar"
    Amritsar = "Amritsar"
    Ahmedabad = "Ahmedabad"
    Trichy = "Trichy"
    Pune = "Pune"
    Calicut = "Calicut"


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
        (all, "all"),
    )
