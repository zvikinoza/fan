#!/usr/bin/python3


from sys import argv
try:
    from PyObjCTools import AppHelper
    from Foundation import *
    from AppKit import *
except ImportError:
    print("Failed to import from PyObjC.")
    exit(-1)    

start_time = NSDate.date()

class MenubarNotifier(NSObject):
    state = 'ok'

    def applicationDidFinishLaunching_(self, sender):
        NSLog("Loaded successfully.")
        try:
            display_text = " ".join(argv[1:])
        except IndexError:
            display_text = "Default Text"
        NSLog("Notification is '{}'".format(display_text))

        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.statusItem.setTitle_(display_text)          # argv[1] or "Default Text"
        self.statusItem.setEnabled_(TRUE)                # item is enabled for clicking
        self.statusItem.setAction_('statusItemClicked:') # method called when statusItem is clicked
        self.statusItem.setHighlightMode_(TRUE)          # highlight the item when clicked

        # Get the timer going
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 5.0, self, 'tick:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
        self.timer.fire()

    def tick_(self, notification):
        NSLog("state is {}".format(self.state))

    def statusItemClicked_(self, notification):
        NSLog("Notification was clicked. Goodbye.")
        AppHelper.stopEventLoop()


def main():
    # Hide the dock icon
    info = NSBundle.mainBundle().infoDictionary()
    info["LSBackgroundOnly"] = "1"

    app = NSApplication.sharedApplication()
    delegate = MenubarNotifier.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(-1)
