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
import tarfile
import colorsys

ROOT = Path(__file__).resolve().parent


def material_values(palette, material):
    """Evaluate the shell's small color-token grammar into QML color values."""
    def color(expression):
        expression = expression.strip()
        if expression.startswith('@'):
            text = palette[expression[1:].replace('-', '_')]
            return tuple(int(text[i:i + 2], 16) / 255 for i in (1, 3, 5)) + (1.,)
        function, body = expression.split('(', 1)
        body = body[:-1]
        arguments, start, depth = [], 0, 0
        for index, char in enumerate(body):
            depth += (char == '(') - (char == ')')
            if char == ',' and depth == 0:
                arguments.append(body[start:index]); start = index + 1
        arguments.append(body[start:])
        first = color(arguments[0]); amount = float(arguments[-1])
        if function == 'alpha':
            return first[:3] + (first[3] * amount,)
        if function == 'mix':
            second = color(arguments[1])
            return tuple(a * (1 - amount) + b * amount for a, b in zip(first, second))
        if function == 'shade':
            hue, light, saturation = colorsys.rgb_to_hls(*first[:3])
            return colorsys.hls_to_rgb(hue, min(1, light * amount), min(1, saturation * amount)) + (first[3],)
        raise ValueError('Unsupported color token: ' + function)
    definitions = {'surface': 'ui-surface', 'hoverSurface': 'ui-surface-hover',
                   'selectedSurface': 'ui-surface-selected', 'border': 'ui-border', 'panel': 'ui-panel'}
    tokens = material['colour']
    values = {name: palette.get(role, palette['surface']) for name, role in dict(accent='accent', foreground='foreground', muted='muted', selectedForeground='selected_fg', popover='popover').items()}
    for name, role in definitions.items():
        expression = tokens[role].replace('{{material.opacity}}', str(material['material']['opacity']))
        values[name] = color(expression)
    measures = dict(controlRadius=material['radius']['control'], cardRadius=material['radius']['card'],
                    padding=material['spacing']['md'], spacing=material['spacing']['sm'],
                    meterHeight=material['control']['meter_height'], thumbSize=material['control']['thumb_size'])
    for name, value in measures.items():
        if type(value) not in (int, float) or not 0 < value <= 128:
            raise ValueError('Invalid shared control measure')
        values[name] = value
    return values


def quick_material(palette, material):
    lines = ['pragma Singleton', 'import QtQuick 2.15', 'QtObject {']
    for name, value in material_values(palette, material).items():
        if isinstance(value, str):
            lines.append(f' readonly property color {name}: "{value}"')
        elif isinstance(value, tuple):
            rgba = ','.join(f'{v:.6g}' for v in value)
            lines.append(f' readonly property color {name}: Qt.rgba({rgba})')
        else:
            lines.append(f' readonly property real {name}: {value}')
    return '\n'.join(lines + ['}']) + '\n'


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
    qml_material = quick_material(palette, material)
    output.mkdir(parents=True, exist_ok=True)
    # Every fixed upstream RGB role is mapped once; state opacity stays in SVG.
    original = {}
    for role, source in {
        'accent': '5294e2 0582ff 5796e8 58acff 4693e6 3176bf',
        'foreground': 'd3dae3 ffffff d7d7d7 b4b4b4 d2d2d2 c3c3c3',
        'muted': '92959d 5a5a5a a0a0a0 787878 767b87 7b7b7b 969696 acb1bc',
        'background': '000000 111217 22252e 262933 2d303b 2d323d 2f343f 1e1e1e 222224 141414 22242e 2b2e39',
        'base': '383c4a 343844 3c404e 363c48 323542 31353f',
        'surface': '404552 4b5162 474d5d 505666 4d5367 444a58 444448 474d5b 5a616e 505050',
        'border': '151515 b74aff',
        'red': 'f04a50',
    }.items():
        original.update({key: role for key in source.split()})
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
    from widgets import render_widgets
    qss = render_widgets(palette, material_values(palette, material), output)
    for version in (5, 6):
        (output / f'qt{version}.conf').write_text(scheme(palette, version, opacity, qt6_extended))
        (output / f'qt{version}.qss').write_text(qss)
    # Own the visual style as well as the palette. Native Templates retain
    # keyboard, pointer, accessibility and data behavior; Fusion fills new types.
    with tarfile.open(ROOT / 'quick.tar.gz') as archive:
        for item in archive:
            relative = Path(item.name)
            if not item.isfile() or relative.is_absolute() or '..' in relative.parts or relative.parts[0] != 'Anto426':
                raise ValueError('Invalid Qt Quick style archive entry')
            target = output / 'qml' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(item).read())
    (output / 'qml/Anto426/Material.qml').write_text(qml_material)
    quick_roles = {'WindowText': 'foreground', 'Text': 'foreground', 'ButtonText': 'foreground',
                   'BrightText': 'foreground', 'Button': 'surface', 'Window': 'background',
                   'Base': 'base', 'AlternateBase': 'base_alt', 'Highlight': 'accent',
                   'HighlightedText': 'selected_fg', 'Link': 'accent', 'LinkVisited': 'purple',
                   'ToolTipBase': 'surface', 'ToolTipText': 'foreground', 'PlaceholderText': 'muted',
                   'Accent': 'accent', 'Light': 'select', 'Midlight': 'border',
                   'Dark': 'background', 'Mid': 'border', 'Shadow': 'background'}
    sections = ['[Controls]\nStyle=Anto426\nFallbackStyle=Fusion']
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
