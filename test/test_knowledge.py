import unittest

from parameterized import parameterized

from grafana_client.knowledge import (
    datasource_factory,
    get_healthcheck_expression,
    query_factory,
)
from grafana_client.model import DatasourceModel

SUPPORTED_DATA_SOURCE_TYPES = [
    "cratedb",
    "elasticsearch",
    "influxdb",
    "influxdb+influxql",
    "influxdb+flux",
    "postgres",
    "prometheus",
    "testdata",
]


SUPPORTED_DATA_SOURCE_TYPES_COMPAT = SUPPORTED_DATA_SOURCE_TYPES.copy()
SUPPORTED_DATA_SOURCE_TYPES_COMPAT.remove("cratedb")


class KnowledgebaseTestCase(unittest.TestCase):
    @parameterized.expand(SUPPORTED_DATA_SOURCE_TYPES)
    def test_datasource_factory_success(self, data_source_type):
        ds = datasource_factory(DatasourceModel(name="foo", type=data_source_type, url=None, access=None))
        self.assertIsInstance(ds, DatasourceModel)

    def test_datasource_factory_unknown_failure(self):
        self.assertRaises(
            NotImplementedError,
            lambda: datasource_factory(DatasourceModel(name="foo", type="unknown", url=None, access=None)),
        )

    @parameterized.expand(SUPPORTED_DATA_SOURCE_TYPES)
    def test_query_factory_success(self, data_source_type):
        ds = datasource_factory(DatasourceModel(name="foo", type=data_source_type, url=None, access=None))
        query = query_factory(ds.asdict(), expression="bar")
        self.assertIsInstance(query, (dict, str))

    def test_query_factory_unknown_type_failure(self):
        ds = datasource_factory(DatasourceModel(name="foo", type="prometheus", url=None, access=None))
        ds.type = "unknown"
        self.assertRaises(
            NotImplementedError,
            lambda: query_factory(ds.asdict(), expression="bar"),
        )

    def test_query_factory_unknown_influxdb_dialect_failure(self):
        ds = datasource_factory(DatasourceModel(name="foo", type="influxdb", url=None, access=None))
        ds.jsonData["version"] = "unknown"
        self.assertRaises(
            KeyError,
            lambda: query_factory(ds.asdict(), expression="bar"),
        )

    @parameterized.expand(SUPPORTED_DATA_SOURCE_TYPES_COMPAT)
    def test_get_healthcheck_expression_all(self, data_source_type):
        result = get_healthcheck_expression(data_source_type)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 1)

    def test_get_healthcheck_expression_influxdb_flux(self):
        result = get_healthcheck_expression("influxdb", "Flux")
        self.assertEqual(result, "buckets()")

    def test_get_healthcheck_expression_unknown_failure(self):
        self.assertRaises(NotImplementedError, lambda: get_healthcheck_expression("foobar"))
