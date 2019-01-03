import requests
import json
import time

API_KEY = ''

# Design a job
#job instructuons must be in HTML format 

def create_job(name, API_KEY):  
    ### Create a new job with name and returns the job id
    '''
        args: API_KEY: fig8 api key
    '''
    with open('data/' + str(path), 'rb') as instructions:

    headers = {'content-type': 'application/json'}
    data = {'job': {'title': name, 'instructions': instructions}}
    job_description = requests.post('https://api.figure-eight.com/v1/jobs.json?key={api_key}'.format(api_key=API_KEY),
                                data=json.dumps(data), headers=headers)
    print(job_description.status_code)
    return json.loads(job_description.content.decode('utf-8'))['id']

def upload_full_data(job_id, API_KEY):
    # upload csv file, can contain TQs just make sure all headers are set up correctly and there are no missing headers
    '''
        args: API_KEY: fig8 api key
    '''
    headers = {'content-type': 'text/csv'}
    with open('sample_data.csv', 'rb') as judgement_file:
        requests.put('https://api.figure-eight.com/v1/jobs/{job_id}/upload.json?key={api_key}&force=true'.format(
            job_id=job_id, api_key=API_KEY), data=judgement_file, headers=headers)

def upload_gold_questions(job_id, API_KEY):
    
    # upload csv file, can contain TQs just make sure all headers are correctly named
    headers = {'content-type': 'text/csv'}
    with open('sample_data_with_tq.csv', 'rb') as judgement_file:
        requests.put('https://api.figure-eight.com/v1/jobs/{job_id}/upload.json?key={api_key}&force=true'.format(
            job_id=job_id, api_key=API_KEY), data=judgement_file, headers=headers)

    # convert uploaded test question
    response = requests.put('https://api.figure-eight.com/v1/jobs/{job_id}/gold.json?key={api_key}'.format(
        job_id=job_id, api_key=API_KEY), headers={'content-type': 'text/csv'})
    print(response.content)

def upload_cml_to_job(job_id, API_KEY):
    # update the cml of the job, find job by its job_id
    with open('test_cml.cml') as cml_file:
        cml_content = cml_file.read()
        response = requests.put('https://api.figure-eight.com/v1/jobs/{job_id}.json?key={api_key}'.format(
            job_id=job_id, api_key=API_KEY), data=json.dumps({'job': {'cml': cml_content}}),
            headers={'content-type': 'application/json'})

def upload_job_meta_data(job_id, API_KEY):
    # add task payment to a job 
    response = requests.put('https://api.figure-eight.com/v1/jobs/{job_id}.json?key={api_key}'.format(
        job_id=job_id, api_key=API_KEY), data=json.dumps({'job': {'payment_cents': 5}}),
        headers={'content-type': 'application/json'})


def start_job(job_id, API_KEY):
    # launch the job, find job by its job_id 
    response = requests.post('https://api.figure-eight.com/v1/jobs/{job_id}/orders.json?key={api_key}'.format(
        job_id=job_id, api_key=API_KEY), data=json.dumps({'channels':{'0':'on_demand'},'debit': {'units_count': 100}}),
        headers={'content-type': 'application/json'})
    print(response.content)