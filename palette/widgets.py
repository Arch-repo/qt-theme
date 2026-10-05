"""Shared shell primitives for Qt Widgets, including complex subcontrols."""
from pathlib import Path


def render_widgets(palette, material, output):
    def rgba(value):
        if isinstance(value, str):
            return value
        return 'rgba(' + ','.join(str(round(channel * 255)) for channel in value) + ')'

    tokens = {key: rgba(value) if isinstance(value, (str, tuple)) else str(value)
              for key, value in material.items()}
    tokens.update(accent=palette['accent'], foreground=palette['foreground'],
                  muted=palette['muted'], selectedForeground=palette['selected_fg'])
    assets = output / 'assets'
    assets.mkdir(exist_ok=True)
    paths = {'check': 'M4 9l3 3 7-7', 'down': 'M4 6l5 5 5-5',
             'up': 'M4 12l5-5 5 5', 'right': 'M6 4l5 5-5 5'}
    for name, path in paths.items():
        for state, color in (('', palette['foreground']), ('-selected', palette['selected_fg'])):
            (assets / (name + state + '.svg')).write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18">'
                f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    (assets / 'radio.svg').write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"><circle cx="9" cy="9" r="4" fill="' + palette['selected_fg'] + '"/></svg>')
    template = (Path(__file__).parent / 'widgets.qss.in').read_text()
    for name, value in tokens.items():
        template = template.replace('@' + name + '@', value)
    return template
