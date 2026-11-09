import re
import dateparser


def extract_date(raw_text: str) -> list:
    """
    Extracts all dates found in a string
    Returns a list of all dates found
    """
    dates = re.findall("[0-9]{2}/[0-9]{2}/20[0-9]{2}", raw_text) # dd/mm/yyyy
    dates.extend(re.findall("20[0-9]{2}/[0-9]{2}/[0-9]{2}", raw_text)) # yyyy/mm/dd
    dates.extend(re.findall("2026[0-9]{4}", raw_text)) # yyyymmdd
    dates.extend(re.findall("[0-9]{2} ?[A-z]{3,9} ?20[0-9]{2}", raw_text)) # dd month yyyy

    if dates:
        date_formats = ["%d/%m/%Y","%Y/%m/%d","%Y%m%d","%d %B %Y","%d %b %Y"]

        for i, date in enumerate(dates):
            dates[i] = dateparser.parse(
                date,
                date_formats=date_formats
            ).strftime("%d/%m/%Y")
        return list(set(dates))

    else:
        return ["NaN"]


def extract_price(raw_text: str) -> float:
    """
    Extracts floats with 2 decimals from a string
    Returns the highest value out of all extracted
    """
    prices = re.findall("[0-9]{1,3}[,|.][0-9]{2}", raw_text)

    # Convert to float
    for index, price in enumerate(prices):
        prices[index] = float(re.sub(",", ".", price))

    # Get highest price on receipt
    prices.sort()
    if prices:
        return prices[-1]
    else:
        return "NaN"
