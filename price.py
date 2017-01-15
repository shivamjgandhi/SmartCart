import requests
import json

def return_name_price_image(word):
	r = requests.get('http://api.walmartlabs.com/v1/search?apiKey=9cbtd8j8r9rzzkhw5pw4pj68&lsPublisherId=sjgandhi1998&query=' + word)
	json_dict = r.json()

	trig = False
	food = 'food'
	key = 0

	for i in range (0, 10):
		cat = json_dict['items'][i]['categoryPath']
		n = len(cat)
		for j in range(0, n-3):
			if cat[j: j+3] is 'food':
				trig = True
				key = i
				break

	item_name = json_dict['items'][key]['name']
	item_price = json_dict['items'][key]['salePrice']
	item_image = json_dict['items'][key]['thumbnailImage']

	n = len(item_name)

	if "oz" in item_name:
		oz_place = item_name.index('oz')
		for k in range(0, oz_place - 2):
	 		if item_name[k] == " ":
	 			space_place = k

	 	item_amount = item_name[space_place + 1:oz_place-1]
	 	item_unit = 'oz'

	elif "lb" in item_name:
	 	lb_place = item_name.index('lb')
	 	for m in range(0, lb_place - 2):
	 		if item_name[m] == " ":
	 			space_place = m

	 	item_amount = item_name[space_place + 1:oz_place-1]
	 	item_unit = 'lb'

	return(item_name, item_price, item_image, item_amount, item_unit)

word = raw_input('What would you like to search? : ')
item_name, item_price, item_image, item_amount, item_unit = return_name_price_image(word);

print(item_name)
print(item_price)
print(item_amount)
print(item_unit)