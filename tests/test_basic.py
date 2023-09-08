import copy
import json

import jsonschema as js
import yaml
from ga4gh.gks.metaschema.tools.source_proc import YamlSchemaProcessor

from config import vrs_json_path, vrs_yaml_path, vrs_merged_yaml_path

# Are the yaml and json parsable and do they match?
p = YamlSchemaProcessor(vrs_yaml_path)
j = json.load(open(vrs_json_path))
m = yaml.safe_load(open(vrs_merged_yaml_path))


def test_json_yaml_match():
    assert p.for_js == j, "parsed yaml and json do not match"


# Can pjs handle this schema?
# def test_pjs_smoke():
#     ob = pjs.ObjectBuilder(pjs_filter(m))
#     assert ob.build_classes()              # no exception => okay

# Does the schema validate against a simple sequence location?
def test_models():
    sl = {
        'sequenceReference': {
            'refgetAccession': 'SQ.9W6SPR3RMCHWCSGJLQHE6KBOD285V5SW',
            'type':'SequenceReference'
        },
        'start': 100,
        'end': [None, 150],
        'type': 'SequenceLocation'
    }
    schema = copy.deepcopy(j)
    schema['$ref'] = '#/$defs/SequenceLocation'
    schema['$id'] = vrs_json_path.as_uri()
    js.validate(sl, schema)

    schema['$ref'] = '#/$defs/Allele'
    a = {
        'location': sl,
        'state': {
            'type': 'ReferenceLengthExpression',
            'length': [32, 35],
            'repeatSubunitLength': 3
        },
        'type': 'Allele'
    }
    js.validate(a, schema)
