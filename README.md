# Fed-cash
Quick and dirty python command line tool to get FEC records from the FEC's API for analyzing Federal campaign finances.

## Installation
1. Clone repo and `cd` into it
2. Start virtual environment
3. Install dependencies with `pip install -r requirements.txt` or `pipenv install`

## Usage
First, you'll need an API key from the FEC and stored as an environment variable as `FEC_API_KEY`.

Then, run
`python parseFEC.py <COMMITTEE_ID> <FILING_TYPE>`

The script will create a folder in 'data/' named after the committee's ID.

### Options
**Filing types**

Type| Description | Use option
--- | --- | ---
Schedule A filings | Itemized recipts given to a committee. Use this to find individual contributors. This does not include contributions less than $200, so use the 'Summary reports' option to get the total for unitemized contributions. | receipts
Schedule B filings | Itemized disbursements, or how the committees are spending their money. | disbursements
Independant Expenditures (Schedule E filings) |  An expenditure for a communication “expressly advocating the election or defeat of a clearly identified candidate that is not made in cooperation, consultation, or concert with, or at the request or suggestion of, a candidate, a candidate’s authorized committee, or their agents, or a political party or its agents.”| ie
Summary reports | Summarized information about a committees finances, included total money raised and spent per filing period. | reports
Filings list | A list of reports filed by the committee to the FEC. | filings

**Committee IDs**

Get this [from the FEC](https://www.fec.gov/data/). IDs typically start with a "C" and some zeros.

**Example committee IDs**
+ NRA Political Victory PAC - C00053553
+ Giffords PAC - C000540443
+ RICK SCOTT FOR FLORIDA - C00676965
+ RICK SCOTT VICTORY FUND - C00676957
+ EVERYTOWN FOR GUN SAFETY ACTION FUND - C90015025

More info on the FEC's API can be found here: https://api.open.fec.gov/developers/

## License 
[MIT](LICENSE.md)