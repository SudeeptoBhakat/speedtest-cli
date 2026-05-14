#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for speedtest-cli."""

import csv
import json
import sys
import os

import pytest

# Add parent directory to path so we can import speedtest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import speedtest


class TestDistance:
    """Test the Haversine distance calculation."""

    def test_same_point(self):
        assert speedtest.distance((0, 0), (0, 0)) == 0.0

    def test_known_distance(self):
        # New York to London ~5570 km
        ny = (40.7128, -74.0060)
        london = (51.5074, -0.1278)
        d = speedtest.distance(ny, london)
        assert 5500 < d < 5700

    def test_antipodal(self):
        # North pole to south pole ~20015 km
        d = speedtest.distance((90, 0), (-90, 0))
        assert 19900 < d < 20100

    def test_equatorial(self):
        # Two points on the equator, 90 degrees apart ~10018 km
        d = speedtest.distance((0, 0), (0, 90))
        assert 9900 < d < 10200


class TestBuildUserAgent:
    """Test user agent string construction."""

    def test_contains_version(self):
        ua = speedtest.build_user_agent()
        assert speedtest.__version__ in ua

    def test_contains_python(self):
        ua = speedtest.build_user_agent()
        assert 'Python/' in ua

    def test_contains_mozilla(self):
        ua = speedtest.build_user_agent()
        assert ua.startswith('Mozilla/5.0')


class TestBuildRequest:
    """Test HTTP request construction."""

    def test_cache_busting(self):
        req = speedtest.build_request('http://example.com/test')
        assert '?x=' in req.get_full_url()

    def test_cache_busting_with_query(self):
        req = speedtest.build_request('http://example.com/test?foo=bar')
        assert '&x=' in req.get_full_url()

    def test_scheme_injection_http(self):
        req = speedtest.build_request('://example.com/test', secure=False)
        assert req.get_full_url().startswith('http://')

    def test_scheme_injection_https(self):
        req = speedtest.build_request('://example.com/test', secure=True)
        assert req.get_full_url().startswith('https://')

    def test_no_cache_header(self):
        req = speedtest.build_request('http://example.com/test')
        assert req.get_header('Cache-control') == 'no-cache'


class TestFakeShutdownEvent:
    """Test the fake shutdown event."""

    def test_is_set_returns_false(self):
        event = speedtest.FakeShutdownEvent()
        assert event.is_set() is False

    def test_isSet_returns_false(self):
        event = speedtest.FakeShutdownEvent()
        assert event.isSet() is False


class TestSpeedtestResults:
    """Test the results container class."""

    def _make_results(self):
        return speedtest.SpeedtestResults(
            download=100000000,
            upload=50000000,
            ping=15.5,
            jitter=2.3,
            server={
                'id': '1234', 'sponsor': 'Test ISP',
                'name': 'Test City', 'd': 10.5,
                'country': 'US'
            },
            client={'ip': '1.2.3.4', 'isp': 'TestISP'},
        )

    def test_dict_has_required_keys(self):
        r = self._make_results()
        d = r.dict()
        required = ['download', 'upload', 'ping', 'jitter', 'server',
                     'timestamp', 'bytes_sent', 'bytes_received',
                     'share', 'client']
        for key in required:
            assert key in d

    def test_dict_values(self):
        r = self._make_results()
        d = r.dict()
        assert d['download'] == 100000000
        assert d['upload'] == 50000000
        assert d['ping'] == 15.5
        assert d['jitter'] == 2.3

    def test_json_output(self):
        r = self._make_results()
        j = r.json()
        data = json.loads(j)
        assert data['ping'] == 15.5
        assert data['jitter'] == 2.3

    def test_json_pretty(self):
        r = self._make_results()
        j = r.json(pretty=True)
        assert '\n' in j
        assert '    ' in j

    def test_csv_header(self):
        header = speedtest.SpeedtestResults.csv_header()
        assert 'Ping' in header
        assert 'Jitter' in header
        assert 'Download' in header

    def test_csv_output(self):
        r = self._make_results()
        c = r.csv()
        reader = csv.reader([c])
        row = next(reader)
        assert row[0] == '1234'  # Server ID
        assert '15.5' in row[5]  # Ping
        assert '2.3' in row[6]   # Jitter

    def test_csv_custom_delimiter(self):
        r = self._make_results()
        c = r.csv(delimiter='\t')
        assert '\t' in c


class TestVersion:
    """Test version string."""

    def test_version_format(self):
        parts = speedtest.__version__.split('.')
        assert len(parts) == 3

    def test_version_is_3(self):
        assert speedtest.__version__.startswith('3.')


class TestHTTPUploaderData:
    """Test the upload data generator."""

    def test_pre_allocate(self):
        data = speedtest.HTTPUploaderData(
            length=1024, start=0, timeout=10
        )
        data.pre_allocate()
        assert data._data is not None

    def test_len(self):
        data = speedtest.HTTPUploaderData(
            length=2048, start=0, timeout=10
        )
        assert len(data) == 2048
