// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.BusyIndicator {
 id: control
 implicitWidth: 40; implicitHeight: 40
 contentItem: Item {
  opacity: control.running ? 1 : 0
  Repeater { model: 8
   Rectangle { width: 4; height: 10; radius: 2; color: Material.accent; opacity: (index+1)/8
    x: parent.width/2-width/2; y: 2
    transform: Rotation { origin.x: 2; origin.y: 18; angle: index*45 }
   }
  }
  RotationAnimator on rotation { from: 0; to: 360; duration: 900; loops: Animation.Infinite; running: control.running && control.visible }
 }
}
