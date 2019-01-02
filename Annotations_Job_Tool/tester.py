from google_handler import *
from report_handler import *
from smartlogic_handler import *
# from fig8_handler import *
from s3_handler import *

# from api_example import figure8_handler
import csv
import requests
import json
import time



# g_d = Google_handler()
#print (g_d.get_id('telco_tmobile','1M28OzKiFVK9WaQAqjIXOmHk-Vt43rg8YrULjRGIX1zA', 'instructions'))
# print (g_d.download_file('1M28OzKiFVK9WaQAqjIXOmHk-Vt43rg8YrULjRGIX1zA', 'instructions_from_drive.txt', data_type = 'instructions'))
#1NRAHlky18Vq4aQVCj96eYDk8-1vuredQ
#10six9WJQVlD4Zd47qYd7MtALa4Onit7I
#doc - 1M28OzKiFVK9WaQAqjIXOmHk-Vt43rg8YrULjRGIX1zA

# s3_handler = s3_handler()
# s3_handler.host_to_s3('tax.js')
# print(s3_handler.get_file_link('tax.js'))

# session = boto3.Session(
#             aws_access_key_id='AKIAJSFOZIAPAOWR2STA',
#             aws_secret_access_key='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', 
#             region_name = 'us-west-2')
# s3_resource = session.resource('s3')
# first_bucket_name = 'taxonomies-lp'
# s3_resource.Object(first_bucket_name, 'tax.js').upload_file(
#         Filename='tax.js')



instructions = """<script src="//cf-83774kd99dl.s3.amazonaws.com/js_taxonomy_scripts/LP_tax_1.js" type="text/javascript"></script>
<script src="//cf-83774kd99dl.s3.amazonaws.com/js_taxonomy_scripts/LP_tax_2.js" type="text/javascript"></script>

<h1 dir="ltr">Overview</h1>

<p dir="ltr">In this job, you will be presented with dialogue about a cell phone carrier. Review each line of dialogue and determine the highlighted intent of the consumer so that we can have a greater understanding of the overall intent of the author. Approach each line of dialogue as if you are the store operator (agent), helping the consumer find an answer to their problem.</p>

<h1 dir="ltr">Steps</h1>

<ol>
	<li dir="ltr">Read the individual line of dialogue</li>
	<li dir="ltr">Locate highlighted portion of the dialogue</li>
	<li dir="ltr">Determine what the topic associated with the highlighted portion of the dialogue is according to the given category list</li>
</ol>

<h1 dir="ltr">Rules &amp; Tips</h1>

<ul>
	<li dir="ltr">Assess the dialogue as if you are a store operator helping the consumer find an answer to their problem</li>
	<li dir="ltr">All lines of dialogue should be given a category.</li>
	<li dir="ltr">Dialogue may include grammatical errors, missing words or phrases, or symbols. Use your best judgement based on the context of the surrounding language to determine classifications</li>
	<li dir="ltr">Dialogue may include foreign languages. Please translate dialogue and use your best judgement based on the context of the language to determine classifications</li>
	<li dir="ltr">Redacted information such as person names or phones will be replaced with |||person||| or |||digits|||</li>
	<li dir="ltr">Netflix is a promotion, not a service</li>
	<li dir="ltr">JUMP and ONE are plans, not a service</li>
	<li dir="ltr">A phone line (or "line") is a line not a service, device or plan</li>
	<li dir="ltr">A SIM card is a device, not a service</li>
	<li dir="ltr">Data and Insurance are types of services</li>
	<li dir="ltr">Hotspot is a device, not service or network</li>
	<li dir="ltr">If a specific line of dialogue does not fit into a given category or is unable to be categorized in general, please choose “Other”</li>
	<li dir="ltr">If a specific line of dialogue does not have an intention, please choose “Not Intent”. Examples of “Not Intent” are: “Hi?” and “It is Hot outside”</li>
</ul>

<h1 dir="ltr">Category Definitions:</h1>

<table>
	<tbody>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Definition</strong></p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Adjustment To Existing Service Or Product</strong></p>

				<p dir="ltr"><span data-sheets-userformat='{"2":15233,"3":{"1":0},"10":2,"11":4,"12":0,"14":[null,2,0],"15":"Arial","16":11}' data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Descriptions of consumer's seeking to adjust, alter, or modify consumer account information &quot;}">Descriptions of consumer's seeking to adjust, alter, or modify consumer account information&nbsp;</span></p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Information Request For Service Or Product</strong></p>

				<p dir="ltr">Descriptions of consumer's seeking information about services or products</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Purchase or Upgrade a Service Or Product</strong></p>

				<p dir="ltr">Descriptions of the purchasing, adding, or upgrading of products (phones, tablets, smart watches) and services</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Solve Existing Service Or Product Problem</strong></p>

				<p dir="ltr">Descriptions of requests to solve a problem for a service or product</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Suspend Remove Or Cancel Existing Service Or Product</strong></p>

				<p dir="ltr">Descriptions of suspending, removing, canceling, ending, or stopping an existing service or product</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Not Intent</strong></p>

				<p dir="ltr">Descriptions that do not have an intent</p>
			</td>
		</tr>
	</tbody>
</table>

<p>
	<br>
</p>

<h1 dir="ltr">Examples:</h1>

<p>
	<br>
</p>

<table>
	<tbody>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Category</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Good Example</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Reason</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Bad Example</strong></p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Adjustment To Existing Service Or Product</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">" Is it possible for me to switch my my account password"</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">They are trying to modify the a part of the account that specifically relates to the consumer</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">"I want to add a user to the account"</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Information Request For Service Or Product</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">“I was wondering how much a new phone would cost?”</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">They are asking about an information related to the price of a phone</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">“My phone isn’t working when I’m traveling out of state? ”</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Purchase or Upgrade a Service Or Product</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">“Can I add a line to my plan?”</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">The main subject of this statement is about adding a line to the consumer’s account</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">“Does my family plan include 5 lines?”</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Solve Existing Service Or Product Problem</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">“I’m trying to access a feature on my app and it is showing an error”</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">They are stating the error (or issue) is getting in the way the of the consumer using the app</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">“ I am online trying to pay my bill, and want to change my payment option ”</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Suspend Remove Or Cancel Existing Service Or Product</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">"I'm traveling for a few months and don't need my phone, can I suspend the service?"</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">They are requesting help to alter the service status on the account by suspending it.</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">"I want to add a user to my account"</p>
			</td>
		</tr>
		<tr>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr"><strong>Not Intent</strong></p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">“And that is the reason"</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">

				<p dir="ltr">There is no context here to decide what the consumer is looking for</p>
			</td>
			<td style="text-align: center; vertical-align: middle;">
				<br>
			</td>
		</tr>
	</tbody>
</table>
"""

# g_8 = figure8_handler()

# g_8.create_job('test_job_1', instructions, '2B3PrX2NVQzCBJN5Byd6')
# headers = {'content-type': 'application/json'}
# data = {'job': {'title': name, 'instructions': open('data/' + str(path), 'rb')}}
# job_description = requests.post('https://api.figure-eight.com/v1/jobs.json?key={api_key}'.format(api_key=API_KEY, data=json.dumps(data), headers=headers))
# print(job_description.status_code)