import requests
import random
import re

def create_countries_list():

    data = request_data()
    countries = []
    for country in data:
        # get the country common names
        name = country["name"]["common"]

        # Very special case for Sao Tome and Principe, because it uses strange characters
        if name == "São Tomé and Príncipe":
            name = "Sao Tome and Principe"
        
        # get the country flag descriptions
        flag_description = country.get("flags", {}).get("alt", "") # if has no description, just put ""

        # if a country does not have a flag description, skip the rest of the loop
        if not flag_description:
            continue

        # change the prefix of the flag description from (for example: The flag of Afghanistan...) to "This flag..."
        flag_description = change_prefix(name, flag_description)

        # check if flag description contains a spoiler. if so, hide the spoiler
        flag_description = hide_spoiler(name, flag_description)

        # now build an answer set for this country that includes it's common name, plus any alternate spellings/abbreviations
        answer_set = {normalize(name)}
        for alt_spelling in country.get("altSpellings", []):
            answer_set.add(normalize(alt_spelling))

        # add to answer set for countries that need it
        answer_set = add_to_answer_set(name, answer_set)

        # finally append a tuple of the country's name, flag description, and the answer set
        countries.append((name, flag_description, answer_set))

    # must add the three exceptions with no flag descriptions (kosovo, palestine, taiwan)
    countries.append(("Palestine", 
                      "This flag consists of three equal horizontal stripes from top to bottom of black, white, and green and a red triangle with its base along the hoist.", 
                      {"palestine", "ps", "stateofpalestine"}))
    countries.append(("Taiwan",
                      "This flag consists of a red field with a blue canton bearing a white disk surrounded by twelve triangles.", 
                      {"taiwan", "tw", "republicofchina", "中華民國", "zhōnghuámínguó"}))
    countries.append(("Kosovo", 
                      "This flag shows six white stars in an arc above a golden map of the country, all on a blue field", 
                      {"kosovo", "xk", "republicofkosovo", "republikaekosovës", "republikakosova", "pепубликаkосово"}))

    random.shuffle(countries)
    return countries

def request_data():
    response = requests.get(
        "https://restcountries.com/v3.1/all",
        params={"fields": "name,flags,altSpellings"}
    )
    response.raise_for_status() # error check
    return response.json()

def change_prefix(name, desc):
    
    # special case for afghanistan
    if desc.startswith(f"The flag of the Islamic Emirate of Afghanistan"):
        prefix = f"The flag of the Islamic Emirate of Afghanistan"
    
    # special case for drc
    elif desc.startswith(f"The flag of the Democratic Republic of the Congo"):
        prefix = f"The flag of the Democratic Republic of the Congo"

    # special case for usa
    elif desc.startswith(f"The flag of the United States of America"):
        prefix = f"The flag of the United States of America"

    # normal case 1 (The flag of ...)
    elif desc.startswith(f"The flag of {name}"):
        prefix = f"The flag of {name}"

    # normal case 2 (The flag of the ...)
    elif desc.startswith(f"The flag of the {name}"):
        prefix = f"The flag of the {name}"

    else:
        prefix = ""

    return f"This flag{desc[len(prefix):]}"

def hide_spoiler(name, desc):
    # NOTE: Weird case with 'São Tomé and Príncipe'. It just had South Sudan's description for some reason
    # Others just specified that the Union Jack was the flag of the UK, and I didn't like that
    # The rest were all just blatant spoilers
    
    if name == "Andorra" or name == "Brunei" or name == "Croatia" or name == "Iran" or name == "Montenegro" or name == "Oman" or name == "Portugal" or name == "Serbia" or name == "Slovakia":
        desc = desc.replace(f"{name}", "the country")

    elif name == "Australia" or name == "Fiji" or name == "New Zealand" or name == "Tuvalu":
        desc = desc.replace("the flag of the United Kingdom — the Union Jack —", "the Union Jack")

    elif name == "Cyprus":
        desc = "This flag has a white field, at the center of which is a copper-colored silhouette of the country above two green olive branches crossed at the stem."

    elif name == "Ecuador":
        desc = "This flag is composed of the horizontal bands of yellow, blue and red, with the yellow band twice the height of the other two bands. The country's coat of arms is superimposed in the center of the field."

    elif name == "Egypt":
        desc = "This flag is composed of three equal horizontal bands of red, white and black, with the country's national emblem — a hoist-side facing gold eagle of Saladin — centered in the white band."

    elif name == "Lesotho":
        desc = "This flag is composed of three horizontal bands of blue, white and green in the ratio of 3:4:3. A black mokorotlo is centered in the white band."

    elif name == "Switzerland":
        desc = "This flag is square shaped. It features a white cross centered on a red field."

    elif name == "Sao Tome and Principe":
        desc = "This flag is composed of a horizontal triband of green, yellow, and green, with a red isosceles triangle at the hoist and two five-pointed black stars on the yellow band."

    elif name == "Zimbabwe":
        desc = "This flag is composed of seven equal horizontal bands of green, yellow, red, black, red, yellow and green, with a white isosceles triangle superimposed on the hoist side of the field. This triangle is edged in black, spans about one-fourth the width of the field and has its base on the hoist end. A yellow bird superimposed on a five-pointed red star is centered in the triangle."

    return desc

def add_to_answer_set(name, answers):
    if name == "Central African Republic":
        answers.add("car")
    elif name == "DR Congo":
        answers.add("democraticrepublicofthecongo")

    return answers

def normalize(s):
    return re.sub(r"[\s\-]", "", s).lower()

# for testing ----------------------------------------
def print_countries(c):
    # for alphabetical order:
    c.sort(key=lambda item: item[0])

    for count, (name, flag_description, answer_set) in enumerate(c, start=1):
        print(f"({count}) {name}: {flag_description}")
        print(f"        {answer_set}")
        print()
# ----------------------------------------------------