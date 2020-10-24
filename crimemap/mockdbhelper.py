class MockDBHelper:
    def connect(self, database='crimemap'):
        pass

    def get_all_inputs(self):
        return []

    def add_input(self, data):
        pass

    def clear_all(self):
        pass

    def add_crime(self, category, date, latitude, longitude, description):
        pass

    def get_all_crimes(self):
        return [{
            'latitude': 30.604,
            'longitude': 113.247,
            'date': '2020-10-23',
            'category': 'mugging',
            'description': 'mock description'
        },
            {
                'latitude': 30.604,
                'longitude': 113.347,
                'date': '2020-10-24',
                'category': 'mugging',
                'description': 'mock description'
            }
        ]
