# response-differ

response-differ is a python script, which compares responses and prints the result as a unified diff into the console.

## Usage

### Run locally

#### Prerequisite
* [Python](https://www.python.org/) is installed
* [pip](https://pip.pypa.io/en/stable/installation/) is installed

#### Install dependencies
```commandline
pip install -r requirements.txt
```

#### Run response-differ
```commandline
python main.py -u http://example.com/one http://example.com/two
```

### Docker

#### Prerequisite
* [Docker](https://www.docker.com/) is installed.

#### Build the image
```commandline
docker build -t response-differ .
```

#### Run it
```commandline
docker run --rm response-differ --urls http://example.com/one http://example.com/two
```

# Description
The script accepts an even amount of urls in the `-u` flag. Two URLs are handled as a pair.
The first URL is paired with the second one, the third with the fourth and so on.
In each pair, both URLs are requested and the responses are compared.
The result is printed as a unified diff into the console.

## Support
Currently, only plain GET requests are supported.

If the response does not include the `Content-Type` header with `application/json`,
the application will terminate with an error.
