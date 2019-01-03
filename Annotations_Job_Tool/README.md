### Annotations Job Tool

The purpose of this tool is to be a one stop shop for a taxonomist to run an annotation job

Workflow:
Using google drive handler - Download instructions from drive, gold questions and full_data
Using SmartLogic handler - Download Hierarchal report with details from the smartlogic server and create a .js file
Using Figure8 handler - create a job, upload data and instructions, create CML using the scripts
Framework ipynb has the code for cml creation and instructions
Using s3 handler - Upload the .js file on an s3 bucket and update the instructions with the source urls
