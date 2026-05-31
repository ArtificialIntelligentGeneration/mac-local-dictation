import Foundation
import CoreGraphics

func typeText(_ text: String) {
    let source = CGEventSource(stateID: .hidSystemState)
    
    guard source != nil else {
        print("Error: No HID System State source.")
        return
    }

    for char in text.utf16 {
        var utf16Char = char
        if let eventDown = CGEvent(keyboardEventSource: source, virtualKey: 0, keyDown: true) {
            eventDown.keyboardSetUnicodeString(stringLength: 1, unicodeString: &utf16Char)
            eventDown.post(tap: .cghidEventTap)
        }
        
        if let eventUp = CGEvent(keyboardEventSource: source, virtualKey: 0, keyDown: false) {
            eventUp.keyboardSetUnicodeString(stringLength: 1, unicodeString: &utf16Char)
            eventUp.post(tap: .cghidEventTap)
        }
        
        Thread.sleep(forTimeInterval: 0.002)
    }
}

let args = CommandLine.arguments.dropFirst().joined(separator: " ")
if !args.isEmpty {
    typeText(args)
}
