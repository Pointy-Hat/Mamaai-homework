# Server for PDF parsing
## Description
This is a basic server for retrieving text from pdf files. An uploaded file is read and returned as 
a list of text chunks.
## Requirements
This project requires the latest version of **Flask** and **pdfparse.six**. They will install automatically 
when following the steps in the section Setup
## Setup
* For local development, run ```pip install -e ./pdfparse```
* For development in docker, run ```docker-compose build pdf-parse-server```
## Run the server
* Locally, run ```python pdfparse/run_app.py```
* In docker, run ```docker-compose up pdf-parse-server```
The server will listen at the port `localhost:8000`
## Usage
* For simple use without saving, upload a file using `PUT` request at the endpoint `/`. 
The request must contain a valid pdf file.
  * Example usage: `curl -i -X PUT -F file=@tests/data/sample.pdf localhost:8000/`
* To upload and save the file use `POST` request.
  * Example usage: `curl -i -X POST -F file=@tests/data/sample.pdf localhost:8000/`
* To list existing files, use `GET` request at the endpoint `/saved`
* To access/delete a parsed text of a saved file again, use `GET/DELETE` request at `/saved/<filename>`
## Tests
For testing, run the file `tests/test_api.py` using PyTest.
## Comments
Since this is only a quick project, a number of things had to be omitted. These include
* Security
  * The only current deployment type is through `flask.run()` command that has no built-in security.
      For deployment in production this should be changed.
  * There is very little input security, and malicious files with pdf headers could get through.
* `GET` method at `/` endpoint should contain an API summary.
* Saved files should be stored in a database, not in a directory. This database could also contain 
parsed versions, as a some sort of cache.
* Testing files are hard-coded. That could be done in a more modular manner.