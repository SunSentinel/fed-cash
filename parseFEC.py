# A command line tool to grab and parse FEC data for a given committee.
import requests
import json
import csv
import sys
import os
from datetime import datetime

from collections import OrderedDict



API_KEY = os.environ['FEC_API_KEY']

SCHED_A_FIELDS = ["committee_id", "report_year", "report_type", "fec_election_type_desc", "contributor_name", "contributor_street_1", "contributor_city", "contributor_state", "contributor_occupation", "contributor_employer", "contribution_receipt_amount", "receipt_type", "contribution_receipt_date", "file_number", "receipt_type_full", "entity_type_desc", "contributor_aggregate_ytd","two_year_transaction_period","amendment_indicator_desc", "transaction_id", "pdf_url"]
SCHED_B_FIELDS = ["committee_id","report_year","report_type","image_number","line_number","transaction_id","file_number","entity_type","entity_type_desc","unused_recipient_committee_id","recipient_committee_id","recipient_name","recipient_state","beneficiary_committee_name","national_committee_nonfederal_account","disbursement_type","disbursement_type_description","disbursement_description","memo_code","memo_code_full","disbursement_date","disbursement_amount","candidate_office","candidate_office_description","candidate_office_district","candidate_id","candidate_name","candidate_first_name","candidate_last_name","candidate_middle_name","candidate_prefix","candidate_suffix","candidate_office_state","candidate_office_state_full","election_type","election_type_full","fec_election_type_desc","fec_election_year","amendment_indicator","amendment_indicator_desc","schedule_type_full","load_date","original_sub_id","back_reference_transaction_id","back_reference_schedule_id","semi_annual_bundled_refund","payee_last_name","payee_first_name","payee_middle_name","category_code","category_code_full","conduit_committee_name","conduit_committee_street1","conduit_committee_street2","conduit_committee_city","conduit_committee_state","conduit_committee_zip","filing_form","link_id","recipient_city","recipient_zip","disbursement_purpose_category","memo_text","two_year_transaction_period","schedule_type","sub_id","pdf_url","line_number_label","payee_prefix","payee_suffix","payee_employer","payee_occupation","ref_disp_excess_flg","comm_dt"]
SCHED_E_FIELDS = ["committee_id","image_number","line_number","file_number","payee_name","payee_first_name","payee_middle_name","payee_last_name","payee_street_1","payee_street_2","payee_city","payee_state","payee_zip","expenditure_description","expenditure_date","dissemination_date","expenditure_amount","office_total_ytd","category_code","support_oppose_indicator","memo_code","candidate_id","candidate_name","candidate_prefix","candidate_first_name","candidate_middle_name","candidate_suffix","candidate_office","cand_office_state","cand_office_district","notary_sign_date","back_reference_transaction_id","back_reference_schedule_name","filer_first_name","filer_middle_name","filer_last_name","transaction_id","payee_prefix","payee_suffix","memo_text","filer_prefix","filer_suffix","pdf_url"]
date = datetime.now().strftime('%Y%m%d')

def main(committee, filingtype):
    base_url = "https://api.open.fec.gov/v1/"

    # Schedule B filings
    if filingtype == 'disbursements':
        print('Getting disbursements for {0}'.format(committee))
        get_disbursements(base_url, committee)

    elif filingtype == "receipts":
        print('Getting itemized contributions for {0}'.format(committee))
        get_contributions(base_url, committee)

    # Independent expenditures
    elif filingtype == 'ie':
        print('Getting outside spending for {0}'.format(committee))
        get_outside_spending(base_url, committee)

    # Official reports filed to FEC
    elif filingtype == 'filings':
        print('Getting filings for {0}'.format(committee))
        get_filings(base_url, committee)

    # Key financial summary reports
    elif filingtype == 'reports':
        print('Getting report summaries for {0}'.format(committee))
        get_reports(base_url, committee)

    else:
        print('No report type given: Input either disbursements, ie, filings or reports.')


def get_disbursements(url, committee):

    search_params = {
        "api_key": API_KEY,
        "per_page": "100",
        "committee_id": committee
    }

    endpoint_url = url + "schedules/schedule_b/"
    req = requests.get(endpoint_url, search_params)
    results = req.json()
    print(req.url)

    num_pages = results["pagination"]["pages"]
    print("Searching {0} pages...".format(num_pages))

    # Interate through response pages.
    entries = []
    page_num = 1
    while(page_num <= num_pages):
        print("Getting page {0}.".format(page_num))
        search_params["page"] = page_num
        resp = requests.get(endpoint_url, search_params)
        page_data = resp.json()
        page_entries = page_data["results"]
        for entry in page_entries:
            d = [entry[field] for field in SCHED_B_FIELDS]
            entries.append(d)
        page_num = page_num + 1

    save_results(entries, committee, "sb", SCHED_B_FIELDS)

def get_contributions(url, committee):

    search_params = {
        "api_key": API_KEY,
        "per_page": "100",
        "committee_id": committee
    }

    endpoint_url = url + "schedules/schedule_a/"
    req = requests.get(endpoint_url, search_params)
    results = req.json()
    print(req.url)

    num_pages = results["pagination"]["pages"]
    print("Searching {0} pages...".format(num_pages))

    # Interate through response pages.
    entries = []
    page_num = 1
    while(page_num <= num_pages):
        print("Getting page {0}.".format(page_num))
        search_params["page"] = page_num
        resp = requests.get(endpoint_url, search_params)
        page_data = resp.json()
        page_entries = page_data["results"]
        for entry in page_entries:
            d = [entry[field] for field in SCHED_A_FIELDS]
            entries.append(d)
        page_num = page_num + 1

    save_results(entries, committee, "sa", SCHED_A_FIELDS)


def get_outside_spending(url, committee):

    search_params = {
        "api_key": API_KEY,
        "per_page": "100",
        "committee_id": committee,
    }

    endpoint_url = url + "schedules/schedule_e/efile/"
    req = requests.get(endpoint_url, search_params)
    results = req.json()
    print(req.url)

    num_pages = results["pagination"]["pages"]
    print("Searching {0} pages...".format(num_pages))

    # Interate through response pages.
    entries = []
    page_num = 1
    while(page_num <= num_pages):
        print("Getting page {0}.".format(page_num))
        search_params["page"] = page_num
        resp = requests.get(endpoint_url, search_params)
        page_data = resp.json()
        page_entries = page_data["results"]
        for entry in page_entries:
            d = [entry[field] for field in SCHED_E_FIELDS]
            entries.append(d)
        page_num = page_num + 1

    save_results(entries, committee, "se", SCHED_E_FIELDS)


def get_reports(url, committee):
    endpoint_url = url + "committee/{0}/reports/".format(committee)
    search_params = {
        "api_key": API_KEY,
        "per_page": "100",
    }

    req = requests.get(endpoint_url, search_params)
    filings = req.json()
    print(req.url)

    num_pages = filings["pagination"]["pages"]
    print("Searching {0} pages...".format(num_pages))

    filingsData = []
    page_num = 1
    while(page_num <= num_pages):
        print("Got page {0}.".format(page_num))
        search_params["page"] = page_num
        resp = requests.get(endpoint_url, search_params)
        page_data = resp.json()
        page_entries = page_data["results"]
        for filingentry in page_entries:
            d = {}
            d["committee_name"] = filingentry["committee_name"]
            d["document_description"] = filingentry["document_description"]
            d["report_type"] = filingentry["report_type"]
            d["individual_unitemized_contributions_period"] = filingentry["individual_unitemized_contributions_period"]
            d["individual_itemized_contributions_period"] = filingentry["individual_itemized_contributions_period"]
            d["total_individual_contributions_period"] = filingentry["total_individual_contributions_period"]
            d["total_contributions_period"] = filingentry["total_contributions_period"]
            d["total_receipts_period"] = filingentry["total_receipts_period"]
            d["report_year"] = filingentry["report_year"]
            d["coverage_start_date"] = filingentry["coverage_start_date"]
            d["coverage_end_date"] = filingentry["coverage_end_date"]
            d["amendment_indicator_full"] = filingentry["amendment_indicator_full"]
            filingsData.append(d)
        page_num = page_num + 1
    save_results(filingsData, committee, "reports", filingsData[0].keys())


def get_filings(url, committee):
    endpoint_url = url + "committee/{0}/filings/".format(committee)
    search_params = {
        "api_key": API_KEY,
        "per_page": "100",
    }

    req = requests.get(endpoint_url, search_params)
    filings = req.json()
    print(req.url)

    num_pages = filings["pagination"]["pages"]
    print("Searching {0} pages...".format(num_pages))

    filingsData = []
    page_num = 1
    while(page_num <= num_pages):
        print("Got page {0}.".format(page_num))
        search_params["page"] = page_num
        resp = requests.get(endpoint_url, search_params)
        page_data = resp.json()
        page_entries = page_data["results"]
        for filingentry in page_entries:
            d = {}
            d["committee_name"] = filingentry["committee_name"]
            d["report_year"] = filingentry["report_year"]
            d["report_type"] = filingentry["report_type"]
            d["report_type_full"] = filingentry["report_type_full"]
            d["total_receipts"] = filingentry["total_receipts"]
            d["total_individual_contributions"] = filingentry["total_individual_contributions"]
            d["total_independent_expenditures"] = filingentry["total_independent_expenditures"]
            d["total_communication_cost"] = filingentry["total_communication_cost"]
            d["total_disbursements"] = filingentry["total_disbursements"]
            d["cycle"] = filingentry["cycle"]
            d["coverage_start_date"] = filingentry["coverage_start_date"]
            d["coverage_end_date"] = filingentry["coverage_end_date"]
            d["amendment_indicator"] = filingentry["amendment_indicator"]
            d["update_date"] = filingentry["update_date"]
            d["csv_url"] = filingentry["csv_url"]
            filingsData.append(d)
        page_num = page_num + 1

    save_results(filingsData, committee, "filings", filingsData[0].keys())


# Save results to file.
def save_results(data, committee, filing_type, headers):
    print("Writing to file...")

    if not os.path.exists('data/' + committee):
        os.makedirs('data/' + committee)

    with open('data/{0}/{1}_{0}_{2}.csv'.format(committee, date, filing_type), "w") as filingsFile:
        writer = csv.writer(filingsFile)
        writer.writerow(headers)
        for item in data:
            if not (filing_type == 'filings' or filing_type == 'reports'):
                writer.writerow(item)
            else:
                writer.writerow(item.values())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
