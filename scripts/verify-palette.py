#!/usr/bin/env python3
"""Check QPalette role contracts, Kvantum configuration and input validation."""
from pathlib import Path
import configparser
import importlib.util
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('palette', ROOT / 'palette/render.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
PALETTE = json.loads((ROOT / 'palette/default.json').read_text())
MATERIAL = json.loads((ROOT / 'palette/material.json').read_text())


class Palette(unittest.TestCase):
    def test_qt5_fallback_and_qt6_extended_roles(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            renderer.render(PALETTE, MATERIAL, output)
            for version, count in ((5, 21), (6, 22)):
                parser = configparser.ConfigParser()
                parser.read(output / f'qt{version}.conf')
                for group in ('active', 'inactive', 'disabled'):
                    colors = [c.strip() for c in parser['ColorScheme'][group + '_colors'].split(',')]
                    self.assertEqual(len(colors), count)
                    self.assertEqual(colors[20], '#ff' + PALETTE['muted'][1:])
                    self.assertEqual(colors[0][:3], '#ff')
                    self.assertEqual(colors[10][:3], '#75')
                    if version == 6:
                        self.assertEqual(colors[21], '#ff' + PALETTE['accent'][1:])
            config = configparser.ConfigParser(interpolation=None)
            config.read(output / 'anto426.kvconfig')
            self.assertEqual(config['%General']['reduce_window_opacity'], '54')
            self.assertEqual(config['%General']['translucent_windows'], 'true')
            self.assertEqual(config['GeneralColors']['text.color'], 'none')
            self.assertEqual(config['GeneralColors']['window.text.color'], PALETTE['foreground'])
            ET.parse(output / 'anto426.svg')
            quick = (output / 'qtquickcontrols2.conf').read_text()
            self.assertIn('Palette\\Window=#75' + PALETTE['background'][1:], quick)
            self.assertIn('Palette\\Accent=' + '#ff' + PALETTE['accent'][1:], quick)
            renderer.render(PALETTE, MATERIAL, output, qt6_extended=False)
            parser.read(output / 'qt6.conf')
            self.assertEqual(len(parser['ColorScheme']['active_colors'].split(',')), 21)
            self.assertNotIn('Palette\\Accent=', (output / 'qtquickcontrols2.conf').read_text())

    def test_bad_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'theme'
            for palette, material in (({**PALETTE, 'accent': '#broken'}, MATERIAL),
                                      (PALETTE, {**MATERIAL, 'material': {'opacity': True}}),
                                      (PALETTE, {**MATERIAL, 'radius': {'control': '12;'}})):
                with self.assertRaises(ValueError):
                    renderer.render(palette, material, output)
                self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
