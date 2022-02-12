import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def createTable(self, sheetDict: Dict[str, List[str]]):
    """Creates an HTML table template
    TODO at the moment this opens a file and dumps the table code to be copy-paste; will likely need pyppeteer to dump table into email client

    Args:
        sheetDict (dict): A dictionary with the name of the table column as the key, and a list for the table cells

    Unit Tests: TODO
        # Test that a table is created with the correct information inserted
        >>> dict: Dict[str, List[str]] = { "x": ["1", "2"], "y": ["1", "3"] }
        >>> client: GSClient = GSClient()
        >>> client.createTable(dict)
        "<tr><th>x</th><th>y</th></tr><tr><td>1</td><td>1</td></tr><tr><td>2</td><td>3</td></tr>"
    """
    data = ""
    for k, v in sheetDict.items():
        data += "<tr>"
        data += "<th>" + k + "</th>"
        if isinstance(v, list):
            for value in v:
                data += "<td>" + value + "</td>"
        data += "</tr>"
    table = open("table_template.html").read().format(table_contents=data)
    return table