class PaymentMethods:
    FK_WALLET_RUB = 1
    FK_WALLET_USD = 2
    FK_WALLET_EUR = 3
    VISA_RUB = 4
    YOOMONEY = 6
    VISA_UAH = 7
    MASTERCARD_RUB = 8
    MASTERCARD_UAH = 9
    QIWI = 10
    VISA_EUR = 11
    MIR = 12
    ONLINE_BANK = 13
    USDT_ERC20 = 14
    USDT_TRC20 = 15
    BITCOIN_CASH = 16
    BNB = 17
    DASH = 18
    DOGECOIN = 19
    ZCASH = 20
    MONERO = 21
    WAVES = 22
    RIPPLE = 23
    BITCOIN = 24
    LITECOIN = 25
    ETHEREUM = 26
    STEAMPAY = 27
    MEGAFON = 28
    VISA_USD = 32
    PERFECT_MONEY_USD = 33


class OrderStatuses:
    NEW = 0
    PAID = 1
    ERROR = 8
    CANCELED = 9


class Currencies:
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    UAH = 'UAH'
    KZT = 'KZT'


class Languages:
    RU = 'ru'
    EN = 'en'
