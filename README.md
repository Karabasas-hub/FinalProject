# FinalProject
Repo for files of the final project - Automated Testing Pipeline.

For the purposes of the project I have written a "Task Manager" API in Python using Flask.
The API has several enpoints for creating, deleting, updating and retrieving tasks based on ID or due date touching all CRUD operations.

The infrastructure to see how the pipeline works is created in AWS using Terraform. 

Docker is installed and configured inside the virtual machine.

The API application is built and launched inside a Docker container inside the VM.

Once that is set-up - the testing pipeline can be launched with a custom selection of tests.

For further information - refer to the documentation:
