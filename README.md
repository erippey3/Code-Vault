# Code-Vault
Code vault, a project to host code snippets for easily reusable pieces of code.

A group project by Riya Nair, Kuhu Pandit, Eric Rippey, Ani Chinta, and Neil Akalwadi

This project takes the form of a website when deployed. It uses Flask as its main backend, interfacing with 
Postgress, ElasticSearch, and Redis.

Deployment locally on any machine outside of the development environment in which this was coded on will be difficult. 
Mainly for the following reasons: 
* Other machines will not have access to the secret.env file which is used by the Flask instance.
* Postgress has not initialized the proper files.
* GitHub Oath is used in this project and any other machine will not have access to the keys used.

It is possible running docker compose up --build in the Website directory may run the site, but most functionality will not work.

If graders would like to see the full demo, I encourage visiting [our website](https://cs3704-code-vault.com).
In order to download files and upload files, the user will need to be logging into a Github account with a VT email. 
I encourage you to try uploading something!!