#!/usr/bin/env python3
"""Render Qt5/Qt6 palette roles and the matching Kvantum control theme."""
from pathlib import Path
import argparse
import configparser
import ctypes
import ctypes.util
import io
import json
import re

ROOT = Path(__file__).resolve().parent


def extended_qt6():
    library = ctypes.util.find_library('Qt6Core')
    if not library:
        return True
    version = ctypes.CDLL(library).qVersion
    version.restype = ctypes.c_char_p
    return tuple(map(int, version().decode().split('.')[:2])) >= (6, 6)


def scheme(palette, qt_major, opacity, qt6_extended=True):
    # QPalette::ColorRole order. PlaceholderText is role 20; Qt 6.6 adds Accent 21.
    roles = ['foreground', 'surface', 'select', 'border', 'background', 'border',
             'foreground', 'foreground', 'foreground', 'base', 'background',
             'background', 'accent', 'selected_fg', 'accent', 'purple', 'base_alt',
             'foreground', 'surface', 'foreground', 'muted']
    if qt_major == 6 and qt6_extended:
        roles.append('accent')
    groups = {}
    for group in ('active', 'disabled', 'inactive'):
        values = list(roles)
        if group == 'disabled':
            for index in (0, 6, 8, 19, 20):
                values[index] = 'muted'
            values[12] = 'border'
            values[13] = 'muted'
        # Window/Base alpha also reaches Qt Quick styles that honor QPalette;
        # Kvantum manages QWidget backgrounds independently from foregrounds.
        groups[group + '_colors'] = ', '.join(f'#{round(255 * (opacity if index == 10 else opacity * .4 if index == 9 else 1)):02x}' + palette[role][1:] for index, role in enumerate(values))
    return '[ColorScheme]\n' + ''.join(key + '=' + value + '\n' for key, value in groups.items())


def render(palette, material, output, qt6_extended=True):
    for name, value in palette.items():
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
            raise ValueError('Invalid palette role: ' + name)
    opacity = material['material']['opacity']
    if type(opacity) not in (int, float) or not 0 < opacity <= 1:
        raise ValueError('Invalid material opacity')
    radius = material['radius']['control']
    if type(radius) not in (int, float) or not 0 < radius <= 64:
        raise ValueError('Invalid control radius')
    output.mkdir(parents=True, exist_ok=True)
    original = {'404552': 'surface', '383c4a': 'base', '4b5162': 'surface',
                '5294e2': 'accent', '0582ff': 'accent', 'b74aff': 'border',
                'd3dae3': 'foreground', 'ffffff': 'foreground', '151515': 'border',
                '000000': 'background', '5796e8': 'accent'}
    svg = re.sub(r'#[0-9a-fA-F]{6}(?![0-9a-fA-F])',
                 lambda match: palette.get(original.get(match[0][1:].lower(), ''), match[0]),
                 (ROOT / 'base.svg').read_text())
    (output / 'anto426.svg').write_text(svg)
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str
    config.read(ROOT / 'base.kvconfig')
    general = config['%General']
    # Kvantum changes only the painted background's opacity, preserving opaque text.
    general.update(author=general.get('author', '') + '; Anto426',
                   comment='Shared wallpaper palette and shell material', composite='true',
                   translucent_windows='true', reduce_window_opacity=str(round((1 - opacity) * 100)),
                   reduce_menu_opacity='0', blurring='false', popup_blurring='false',
                   menu_shadow_depth='0', tooltip_shadow_depth='0')
    colors = config['GeneralColors']
    mapping = {'window.color': 'background', 'base.color': 'base', 'alt.base.color': 'base_alt',
               'button.color': 'surface', 'light.color': 'select', 'mid.light.color': 'border',
               'dark.color': 'background', 'mid.color': 'border', 'highlight.color': 'accent',
               'inactive.highlight.color': 'accent', 'text.color': 'foreground',
               'window.text.color': 'foreground', 'button.text.color': 'foreground',
               'disabled.text.color': 'muted', 'tooltip.text.color': 'foreground',
               'highlight.text.color': 'selected_fg', 'link.color': 'accent',
               'link.visited.color': 'purple', 'progress.indicator.text.color': 'selected_fg'}
    colors.update({key: palette[role] for key, role in mapping.items()})
    # Kvantum derives PlaceholderText by fading text.color. Let qt5ct/qt6ct own
    # that QPalette role instead; their generated schemes include it explicitly.
    colors['text.color'] = 'none'
    for section in config.sections():
        if section in ('%General', 'GeneralColors'):
            continue
        for key in config[section]:
            if key.startswith('text.') and key.endswith('.color'):
                config[section][key] = 'none'
    stream = io.StringIO()
    config.write(stream, space_around_delimiters=False)
    (output / 'anto426.kvconfig').write_text(stream.getvalue())
    qss = f'''/* Owned palette roles; native widget geometry stays in Kvantum. */
QToolTip {{ background-color: {palette['surface']}; color: {palette['foreground']}; border: 1px solid {palette['border']}; border-radius: {radius}px; }}
QMenu::item:selected {{ background-color: {palette['accent']}; color: {palette['selected_fg']}; }}
'''
    for version in (5, 6):
        (output / f'qt{version}.conf').write_text(scheme(palette, version, opacity, qt6_extended))
        (output / f'qt{version}.qss').write_text(qss)
    # Qt Quick has its own style palette; configure documented per-style roles
    # without forcing a style or replacing any QML controls.
    quick_roles = {'WindowText': 'foreground', 'Text': 'foreground', 'ButtonText': 'foreground',
                   'BrightText': 'foreground', 'Button': 'surface', 'Window': 'background',
                   'Base': 'base', 'AlternateBase': 'base_alt', 'Highlight': 'accent',
                   'HighlightedText': 'selected_fg', 'Link': 'accent', 'LinkVisited': 'purple',
                   'ToolTipBase': 'surface', 'ToolTipText': 'foreground', 'PlaceholderText': 'muted',
                   'Accent': 'accent', 'Light': 'select', 'Midlight': 'border',
                   'Dark': 'background', 'Mid': 'border', 'Shadow': 'background'}
    sections = []
    for style in ('Basic', 'Fusion', 'Imagine', 'Material', 'Universal', 'FluentWinUI3'):
        lines = ['[' + style + ']']
        for name, role in quick_roles.items():
            if name == 'Accent' and not qt6_extended:
                continue
            if style == 'Basic' and name == 'Dark':
                role = 'accent'  # Basic uses Dark for checked switches/progress.
            alpha = opacity if name == 'Window' else opacity * .4 if name == 'Base' else 1
            value = f'#{round(alpha * 255):02x}' + palette[role][1:]
            lines.append('Palette\\' + name + '=' + value)
        if style in ('Material', 'Universal'):
            lines += ['Theme=Dark', 'Accent=' + palette['accent'], 'Foreground=' + palette['foreground'],
                      'Background=' + f'#{round(opacity * 255):02x}' + palette['background'][1:]]
        sections.append('\n'.join(lines))
    (output / 'qtquickcontrols2.conf').write_text('\n\n'.join(sections) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--palette', type=Path, required=True)
    parser.add_argument('--material', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--qt6-legacy', action='store_true', help='Force the pre-Qt6.6 palette without Accent')
    args = parser.parse_args()
    render(json.loads(args.palette.read_text()), json.loads(args.material.read_text()), args.output, not args.qt6_legacy and extended_qt6())
