"""Expected function outputs. Useful for tests."""


parse_server_response_output = [
    {"timestamp": "2018-12-20T11:50:48Z",
     "id": "2344",
     "picker": {"id": "14",
                "name": "Joris",
                "active_since": "2018-09-20T08:20:00Z"},
     "article": {"id": "13473",
                 "name": "ACME Bananas",
                 "temperature_zone": "ambient"},
     "quantity": 2},
    {"timestamp": "2018-12-20T11:50:49Z",
     "id": "2345",
     "picker": {"id": "15",
                "name": "Jan",
                "active_since": "2018-11-14T08:20:15Z"},
     "article": {"id": "13473",
                 "name": "ACME Bananas",
                 "temperature_zone": "ambient"},
     "quantity": 2},
    {"timestamp": "2018-12-20T11:51:00Z",
     "id": "2346",
     "picker": {"id": "14",
                "name": "Joris",
                "active_since": "2018-09-20T08:20:00Z"},
     "article": {"id": "41459",
                 "name": "ACME Apples",
                 "temperature_zone": "ambient"},
     "quantity": 1}]

process_events_output = {
    "14": {
        "picker_name": "Joris",
        "active_since": "2018-09-20T08:20:00Z",
        "picks": [
            {"article_name": "ACME BANANAS",
             "timestamp": "2018-12-20T11:50:48Z"},
            {"article_name": "ACME APPLES",
             "timestamp": "2018-12-20T11:51:00Z"}
        ]},
    "15": {
        "picker_name": "Jan",
        "active_since": "2018-11-14T08:20:15Z",
        "picks": [
            {"article_name": "ACME BANANAS",
             "timestamp": "2018-12-20T11:50:49Z"}
        ]}}

sort_by_pickers_output = [
    {'picker_id': '14',
     'picker_name': 'Joris',
     'active_since': '2018-09-20T08:20:00Z',
     'picks': [
         {'article_name': 'ACME BANANAS',
          'timestamp': '2018-12-20T11:50:48Z'},
         {'article_name': 'ACME APPLES',
          'timestamp': '2018-12-20T11:51:00Z'}
     ]},
    {'picker_id': '15',
     'picker_name': 'Jan',
     'active_since': '2018-11-14T08:20:15Z',
     'picks': [
         {'article_name': 'ACME BANANAS',
          'timestamp': '2018-12-20T11:50:49Z'}
     ]
     }]

clean_up_picker_ids_output = [
    {'picker_name': 'Joris',
     'active_since': '2018-09-20T08:20:00Z',
     'picks': [
         {'article_name': 'ACME BANANAS',
          'timestamp': '2018-12-20T11:50:48Z'},
         {'article_name': 'ACME APPLES',
          'timestamp': '2018-12-20T11:51:00Z'}
     ]},
    {'picker_name': 'Jan',
     'active_since': '2018-11-14T08:20:15Z',
     'picks': [
         {'article_name': 'ACME BANANAS',
          'timestamp': '2018-12-20T11:50:49Z'}
     ]}]
