#!/usr/bin/env python3

import json
import logging
import os
from urllib.parse import urlparse

import click
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

# Dealing with SSL Warnings
try:
    import requests.packages.urllib3

    requests.packages.urllib3.disable_warnings()
except Exception:
    pass


def requests_retry_session(
    retries=10,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504, 503, 403),
    session=None,
):
    """Doing requests nicely"""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# Setting up logging with rich
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

# Initializing console for rich
console = Console()

# Setting context settings for click
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


def parse(response, domain):
    # Getting mail security issues

    # Building table
    mailsec_table = Table(
        show_header=True, title=f"Mail Sender Issues - {domain}", title_justify="left"
    )
    mailsec_table.add_column("Code")
    mailsec_table.add_column("Title")
    mailsec_table.add_column("Severity")

    # Parsing out mail security issues
    if response["MailSenderIssues"]:
        for issue in response["MailSenderIssues"]:
            mailsec_table.add_row(str(issue["code"]), issue["title"], issue["severity"])
    else:
        # If no issues, add a row saying so
        mailsec_table.add_row("0", "No issues found!", "N/A")

    # Displaying table
    console.print(mailsec_table)
    console.print("\n")

    # Getting receiver info

    # Building table
    mailreceiver_table = Table(
        show_header=True, title=f"Mail Receiver Stack - {domain}", title_justify="left"
    )
    mailreceiver_table.add_column("Technology")
    mailreceiver_table.add_column("Service")

    # Parsing out mail receiver info
    try:
        if response["MailReceiverIssues"]:
            for issue in response["MailReceiverIssues"]["supplyDetails"]:
                mailreceiver_table.add_row(issue["technology"], issue["technologyType"])
                console.print(mailreceiver_table)
                console.print("\n")
    except Exception:
        pass

    # Getting raw records
    # Building table
    rawrecords_table = Table(
        show_header=True, title="Raw Records", title_justify="left"
    )
    rawrecords_table.add_column("SPF")
    rawrecords_table.add_column("DMARC")
    rawrecords_table.add_column("MX")

    # Parsing out raw records
    try:
        if response["SPFRecord"]:
            spf = str(response["SPFRecord"])
        else:
            # If no spf record, tell us in red
            spf = "[red]None[/red]"
        if response["DMARCRecord"]:
            dmarc = str(response["DMARCRecord"])
        else:
            # If no DMARC record, tell us in red
            dmarc = "[red]None[/red]"
        if response["MailReceiverIssues"]["mxRecordSet"]:
            for mx in response["MailReceiverIssues"]["mxRecordSet"]:
                mx += f" {str(mx)}"

        # Displaying table
        rawrecords_table.add_row(spf, dmarc, mx)
        console.print(rawrecords_table)
    except Exception:
        pass


@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-k",
    "--api-key",
    help="API Key for caniphish.com",
    required=True,
    envvar="CANIPHISH_API_KEY",
)
@click.option(
    "-e",
    "--email",
    help="Email address for caniphish.com",
    required=True,
    envvar="CANIPHISH_EMAIL",
)
@click.option("-s", "--silent", help="Silent mode", is_flag=True)
@click.argument("domain", required=True)
@click.argument("output", required=False, type=click.Path())
def main(api_key, email, silent, domain, output) -> None:
    """caniphish API CLI utility \n
    Outputs results to TTY by default. \n
    If output is specified, results will be saved to a file in JSON format.
    """

    # Target URL for APi request
    target = f"https://caniphish.com/API/SupplyChainScan?emailAddress={email}&apiKey={api_key}&domainName={domain}"
    try:
        # Issuing request
        response = (
            requests_retry_session()
            .get(target, timeout=5, allow_redirects=False, verify=False)
            .json()
        )

        # Dealing with silent flag
        if not silent:
            parse(response, domain)

        # Outputting raw JSON response if specified
        if output:
            if os.path.exists(output):
                with open(output, "a") as f:
                    f.write(json.dumps(response, indent=4))
                    f.write("\n")
            else:
                with open(output, "w") as f:
                    f.write(json.dumps(response, indent=4))
                    f.write("\n")
    except requests.exceptions.RequestException:
        pass


if __name__ == "__main__":
    main()
