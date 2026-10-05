// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.ScrollView {
 id: control
 clip: true
 ScrollBar.vertical: ScrollBar { parent: control; x: control.width-width; y: control.topPadding; height: control.availableHeight; active: control.ScrollBar.horizontal.active }
 ScrollBar.horizontal: ScrollBar { parent: control; x: control.leftPadding; y: control.height-height; width: control.availableWidth; active: control.ScrollBar.vertical.active }
}
