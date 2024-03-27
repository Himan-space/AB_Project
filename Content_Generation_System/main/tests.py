from django.test import TestCase

# Create your tests here.
input_prompt = int(input("Enter question number: "))

if input_prompt > len(prompt_dictionary) or input_prompt <= 0:
    
    while input_prompt > len(prompt_dictionary) or input_prompt <= 0:
        print("Please input the correct question number.")
        input_prompt = int(input("Enter question number: "))

print("\nYou have selected prompt: ", prompt_dictionary[input_prompt]['question'])

input_prompt = prompt_dictionary[input_prompt]['prompt']

for i in range(len(urls_list)):
    print(f"{i+1}. {urls_list[i]}")

indices_input = input("Enter comma-separated indices (-1 to return empty list, 0 for entire list): ")

domains_to_restrict_in_search = get_urls(urls_list, indices_input)
print("Searching following domain: ", domains_to_restrict_in_search)

country_code = input('Enter country code: ("in" for india, if not country specific leave empty): ')
print('Country code: ', country_code)

res = generate_content_piece(input_prompt=input_prompt, country_code=country_code, specific_domains_to_capture=domains_to_restrict_in_search)