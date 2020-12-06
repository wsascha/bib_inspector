import argparse
import logging

import bibtexparser

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)


class Entry:
    def __init__(self, entry_dict):
        self._required_fields = [
            'title',
            'year',
        ]
        self._optional_fields = [
            'doi',
        ]
        self._entry_dict = entry_dict

    def required_fields(self):
        return self._required_fields

    def optional_fields(self):
        return self._optional_fields

    def _missing_fields(self, required_fields, available_fields):
        missing_required_fields = []
        for field in required_fields:
            if field not in available_fields:
                missing_required_fields.append(field)
        return missing_required_fields

    def warn_of_missing_fields(self, optional: bool = False):
        bib_id = self._entry_dict['ID']
        fields_list = list(self._entry_dict.keys())

        def _list_missing_fields(required_fields, log_func):
            missing_required_fields = self._missing_fields(
                required_fields, fields_list)
            if len(missing_required_fields):
                log_func(
                    f'{bib_id} : Missing field(s) {missing_required_fields}.')

        _list_missing_fields(self._required_fields, logging.error)
        if optional:
            _list_missing_fields(self._optional_fields, logging.warning)


class Article(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'author',
        ])

        arxiv_required_fields = [
            'archiveprefix',
            'eprint',
            'url',
            'urldate',
        ]
        arxiv_optional_fields = ['arxivid']

        # Check for any arxiv-related field.
        # If available, assume arxiv entry.
        arxiv_fields = arxiv_required_fields + arxiv_optional_fields
        available_fields = list(self._entry_dict.keys())
        missing_arxiv_fields = self._missing_fields(arxiv_fields,
                                                    available_fields)
        is_arxiv = len(missing_arxiv_fields) < len(arxiv_fields)

        if is_arxiv:
            self._required_fields.extend(arxiv_required_fields)
            self._optional_fields.extend(arxiv_optional_fields)
        else:
            self._required_fields.extend([
                'journal',
                'pages',
            ])
            self._optional_fields.extend([
                'issue',
                'volume',
            ])


class Book(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'author',
            'editor',
            'address',
        ])


class InProceedings(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'address',
            'author',
            'booktitle',
            'pages',
        ])
        self._optional_fields.extend([
            'editor',
            'volume',
        ])


class Manual(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'author',
        ])


class Misc(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'author',
        ])


class PhdThesis(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'address',
            'author',
            'note',
            'school',
        ])


class TechReport(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'institution',
            'location',
            'type',
        ])


class Thesis(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self._required_fields.extend([
            'author',
            'note',
            'school',
        ])


available_entries = {
    'article': Article,
    'book': Book,
    'inproceedings': InProceedings,
    'manual': Manual,
    'misc': Misc,
    'phdthesis': PhdThesis,
    'techreport': TechReport,
    'thesis': Thesis,
}


def make_entry(entry_dict):
    entrytype = entry_dict['ENTRYTYPE']

    if entrytype in available_entries.keys():
        return available_entries[entrytype](entry_dict)
    else:
        logging.warning(f'No customized entry available for {entrytype}!')
        return Entry(entry_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Inspect bib files with required fields.')
    parser.add_argument('-i',
                        metavar='input.bib',
                        nargs=1,
                        type=str,
                        help='Input .bib file')
    parser.add_argument('--optional',
                        nargs='?',
                        type=bool,
                        default=False,
                        help='Show optional warnings')
    args = parser.parse_args()

    fn_in = args.i[0]
    optional_warnings = args.optional

    with open(fn_in) as bibtex_file:
        db = bibtexparser.load(bibtex_file)

    for entry_dict in db.entries:
        entry = make_entry(entry_dict)
        entry.warn_of_missing_fields(optional=optional_warnings)
