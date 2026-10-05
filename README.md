# Anto426 Qt theme

Canonical renderer for the Anto426 wallpaper palette and shared shell material.
One theme covers Qt5 Widgets, Qt6 Widgets and palette-aware Qt Quick Controls.
Kvantum preserves native foreground opacity while painting transparent backgrounds.

```sh
python3 palette/render.py --palette palette/default.json \
  --material palette/material.json --output build/theme
python3 scripts/verify-palette.py
```

The renderer emits separate native color schemes: 21 roles for Qt5, 22 for
Qt6.6+, including PlaceholderText and Accent. Qt6 before 6.6 receives the 21-role
fallback automatically; `--qt6-legacy` forces it for artifact checks. Qt5 support
requires 5.12+ (PlaceholderText). Python 3.10+ is the only renderer dependency.

`anto426.svg` and `anto426.kvconfig` recolor the KvArcDark control base. Kvantum
manages background opacity, never whole-window text opacity. Text roles delegate
to qt5ct/qt6ct where Kvantum would otherwise replace PlaceholderText with faded
foreground. Tooltip/menu backgrounds remain readable.

`qtquickcontrols2.conf` supplies documented per-style palettes to Basic, Fusion,
Imagine, Material, Universal and FluentWinUI3. It does not force a Quick style or
replace QML controls. Application-owned palettes, compiled styles and fully custom
rendering may override these preferences; coverage is not universal Qt-app skinning.

## Desktop installation

The dotfiles installer downloads immutable resources with SHA-256 verification;
its shared installer selects Kvantum, retains fonts/custom stylesheets and exports
`QT_QPA_PLATFORMTHEME=qt5ct`. Current qt6ct accepts this compatible key alongside
Qt5ct. `QT_STYLE_OVERRIDE` is cleared so the platform theme can preserve all roles.
`QT_QUICK_CONTROLS_CONF` points to the generated per-style palette. Existing apps
may require reopening to adopt changed style configuration.

Runtime verified with Qt5 5.15.19, Qt6/Quick 6.11.2 and Kvantum 1.1.8, including
live compositor background-response checks. Older Qt6 is artifact-verified;
an older Qt runtime was not executed on the test host.

Upstream assets and licensing: [UPSTREAM.md](UPSTREAM.md), [LICENSE](LICENSE).
Primary references: [QPalette](https://doc.qt.io/qt-6/qpalette.html),
[Quick palette configuration](https://doc.qt.io/qt-6/qtquickcontrols-configuration.html),
[Kvantum configuration](https://github.com/tsujan/Kvantum/blob/master/Kvantum/doc/Theme-Config).
