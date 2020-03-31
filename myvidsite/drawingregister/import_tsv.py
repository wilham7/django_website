import csv
import requests
import urllib
import json

posturl = 'http://127.0.0.1:8000/dregister/uploadDrawings/'
posturl_sub = 'http://127.0.0.1:8000/dregister/uploadSubmissions/'

def makeDrawings():
	headers = []

	with open("Drawing register.tsv") as tsvfile:
		read = csv.reader(tsvfile, delimiter='\t')
		for row in read:
			headers.append(row)
			# print(row)
		keys = headers[0]
		vals = headers
		del vals[0]

		# print(keys)
		# print('-----------------------')

		all_data = []


		for row in vals:
			x = 0
			row_data = {}

			for v in row:
				val_dict = dict({keys[x]:v})
				row_data.update(val_dict)
				x = x + 1
			all_data.append(row_data)

		print('STARTS HERE ---------------------------------------------------------------------------------')

		good_keys = ['NUMBER - Project','NUMBER - Originator','NUMBER - Volume OR System','NUMBER - Type','NUMBER - Discipline','NUMBER - Series','NUMBER - Level','NUMBER - Zone or Sequence','DRAWING TITLE - Title 1','DRAWING TITLE - Title 2 (Category)','DRAWING TITLE - Title 3','STUDIO RESPONSIBILITY','MODEL LOCATION','REVISION OFFSET','SCALE','PRINT','TYPE','DISCIPLINE','PHASE','ORIGINATOR']

		all_data_new = []

		for i in all_data:
			filtered = dict(zip(good_keys, [i[k] for k in good_keys]))
			all_data_new.append(filtered)

		lut = {"NUMBER - Project":"dn_project","NUMBER - Originator":"dn_originator","NUMBER - Volume OR System":"dn_volume_system","NUMBER - Type":"dn_type","NUMBER - Discipline":"dn_discipline","NUMBER - Series":"dn_series","NUMBER - Level":"dn_level","NUMBER - Zone or Sequence":"dn_zone_sequence","DRAWING TITLE - Title 1":"drawing_title1","DRAWING TITLE - Title 2 (Category)":"drawing_title2","DRAWING TITLE - Title 3":"drawing_title3","STUDIO RESPONSIBILITY":"studio","MODEL LOCATION":"model_location","REVISION OFFSET":"revision_offset","SCALE":"scale","PRINT":"paper","TYPE":"dwg_type","DISCIPLINE":"discipline","PHASE":"phase","ORIGINATOR":"originator"}
		final_data = []

		for d in all_data_new:
			x = 0
			row_adn = {}
			for v in d:
				adn = dict({lut[v]:d[v]})
				row_adn.update(adn)
			final_data.append(row_adn)

		# print(final_data)

		post_data = []

		for d in final_data:
			topost = {'data':json.dumps([d])
			}
			post_data.append(topost)


		for d in post_data:
			try:
				# print(d)
				r = requests.post(posturl, d)
				drawing = r.json()

				print(drawing)
			except Exception as e:
				print(e)



def makeSubs():

	headers = []

	with open("Drawing register.tsv") as tsvfile:
		read = csv.reader(tsvfile, delimiter='\t')
		for row in read:
			headers.append(row)
			# print(row)
		keys = headers[0]
		vals = headers
		del vals[0]	

		# print(vals)

		dnum_list = []

		for row in vals:
			dnum = str(row[1]+'-'+row[2]+'-'+row[3]+'-'+row[4]+'-'+row[5]+row[6]+row[7]+row[8])
			dnum = str(dnum).replace("~","")
			dnum_list.append(dnum)

		# print(dnum_list)

		row_count = 0
		
		new_vals = []

		for row in vals:

			new_row = []

			val_count = 0

			for v in row:
				if v == 'X':
					dn = dnum_list[row_count]
					new_row.append(dn)


					# vals[row_count][val_count].replace('X',dnum_list[row_count])
					# print(vals[row_count][val_count])
					# print(dnum_list[row_count])
				else:
					new_row.append(v)
				val_count += 1
			row_count += 1

			new_vals.append(new_row)

		# print(new_vals)
		out_list = []

		index_count = 0
		for i in keys:
			try:
				x = int(i)
				new_list = []
				date_dict = dict({'sub_date':i,'req_drawings':[]})

				for row in new_vals:
					if row[index_count] != '':
						new_list.append(row[index_count])
				out_list.append(date_dict)
				date_dict['req_drawings'] = new_list
			except Exception as e:
				print(e)
			index_count += 1


		print(out_list)


		post_data = []

		for d in out_list:
			topost = {'data':json.dumps([d])
			}
			post_data.append(topost)


		for d in post_data:
			try:
				# print(d)
				r = requests.post(posturl_sub, d)
				drawing = r.json()

				print(drawing)
			except Exception as e:
				print(e)


makeDrawings()
makeSubs()