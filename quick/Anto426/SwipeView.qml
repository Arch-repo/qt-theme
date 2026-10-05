// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.SwipeView {
 id: control
 implicitWidth: implicitContentWidth; implicitHeight: implicitContentHeight
 contentItem: ListView { model: control.contentModel; interactive: control.interactive; currentIndex: control.currentIndex; orientation: control.orientation; snapMode: ListView.SnapOneItem; boundsBehavior: Flickable.StopAtBounds; highlightRangeMode: ListView.StrictlyEnforceRange; highlightMoveDuration: 180; clip: true }
}
