<div align="center">

# cipcli

cipcli is a utility for extracting information from the [caniphish.com](https://caniphish.com) API.

<br>

[Installation](#installation) •
[Getting started](#getting-started) •
[Usage](#usage) •
[Coming Soon](#coming-soon) •
[Thanks](#Thanks)

</div><br>

</div>
<br>

## Installation

cipcli can be installed for the PyPi using the following command:

```
pipx install cipcli
```

If this tool is not yet availible via PyPi, you can install it directly from the repository using:

```
pipx install git+https://github.com/puzzlepeaches/cipcli.git
```

or

```
git clone ttps://github.com/puzzlepeaches/cipcli.git && cd cipcli
pip3 install .
```

For development, clone the repository and install it locally using poetry.

```
git clone https://github.com/puzzlepeaches/cipcli.git
cd cipcli
poetry shell
poetry install
```

<br>

## Getting started

You need a caniphish API key to use this tool. You can get one by signing up for a free account at [caniphish.com](https://caniphish.com).

Follwing this, set the API key and the email you used for the account as an environment variable.

```
export CANIPHISH_API_KEY=your_api_key
export CANIPHISH_EMAIL=your_email
```

<br>

Once this is setup, you can use the utility by running either of the following commands:

```
cipcli
caniphishcli
```

cipcli provides the option to output API responses as a rich table, to a JSON file or both. If you want the output to just go to a file, use the `--silent` flag.

## Usage

The help menu for the utility is shown below:

```
Usage: cipcli [OPTIONS] DOMAIN [OUTPUT]

  caniphish

Options:
  -k, --api-key TEXT  API Key for caniphish.com  [required]
  -e, --email TEXT    Email address for caniphish.com  [required]
  -s, --silent        Silent mode
  -h, --help          Show this message and exit.
```

<br>

## Coming Soon

Some planned features coming in the next release:

- Parsing for `directMailSpool` and `vulnerable` fields

<br>

## Thanks

Thanks to [caniphish.com](https://caniphish.com) for providing the API and info.
