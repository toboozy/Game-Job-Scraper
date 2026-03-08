"""This script performs conversions on string values to format them for the database. 
    This ensures all values in the database will be presented the same way, which is essential for effective SQL queries."""

MONTHS = {'january':'1', 'february':'2', 'march':'3', 'april':'4', 'may':'5', 'june':'6', 'july':'7', 
              'august':'8', 'september':'9', 'october':'10', 'november':'11', 'december':'12'}

PUNCT = '!()-[];:",<>.?@#$%^&*_~'


def strip_alpha(text : str):
    for c in text:
        if (c.isalpha()):
            text = text.replace(c,'')
    
    return text


def strip_punct(text : str):
    
    for c in text:
        if (c in PUNCT):
            text = text.replace(c,'')
    
    return text


# Converts a month represented as a word to it's integer counterpart
# Eg. March returns '03', April
def convert_month_to_number(date : str):
    for month in MONTHS:
        if (month in date.lower().strip()):
            return MONTHS[month]    


# Returns a text string date in standerdized ISO format (YYYY-MM-DD)
def date_ISO(date : str, input_format : str):
    # TO DO: use substrings with input_format to remove manual if statement implementation
    # NOTE: this current implementation might cause issues with an input date where the day is specified as text like 'Monday 22, March, 1990'

    if input_format == 'MM-DD-YYYY': 
        converted_date = strip_punct(date).strip().split()
        try:
            day = int(converted_date[1]) 
            month = int(convert_month_to_number(converted_date[0]))
            year = int(converted_date[2])
            return f'{year}-{month:02d}-{day:02d}' 
        except ValueError:
            print('Unable to convert date as a value could not be converted to a number.')
            print(f'Input Date: {date}')
            print(f'Output Date: {year}-{month}-{day}')
            return
        

    