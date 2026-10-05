// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
Rectangle {
 property bool highlighted: false
 property bool pressed: false
 property bool hovered: false
 property bool focused: false
 property bool flat: false
 radius: Material.controlRadius
 color: highlighted ? Material.accent : pressed ? Material.selectedSurface : hovered ? Material.hoverSurface : flat ? "transparent" : Material.surface
 border.width: flat && !focused ? 0 : 1
 border.color: focused ? Material.accent : highlighted ? "transparent" : Material.border
 opacity: enabled ? 1 : 0.45
 Behavior on color { ColorAnimation { duration: 100 } }
}
