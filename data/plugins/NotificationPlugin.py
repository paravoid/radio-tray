##########################################################################
# Copyright 2009 Carlos Ribeiro
#
# This file is part of Radio Tray
#
# Radio Tray is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 1 of the License, or
# (at your option) any later version.
#
# Radio Tray is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radio Tray.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################


from radiotray.Plugin import Plugin
from radiotray.lib.common import APP_ICON, APPNAME
from radiotray.events.EventManager import EventManager

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Notify
from gi.repository import GdkPixbuf

class NotificationPlugin(Plugin):

    def __init__(self):
        super(NotificationPlugin, self).__init__()

    def getName(self):
        return self.name

    def initialize(self, name, notification, eventSubscriber, provider, cfgProvider, mediator, tooltip):
    
        self.name = name
        self.notification = notification
        self.eventSubscriber = eventSubscriber
        self.provider = provider
        self.cfgProvider = cfgProvider
        self.mediator = mediator
        self.tooltip = tooltip
        

    def activate(self):
        self.notif = None
        self.lastMessage = None
        self.eventSubscriber.bind(EventManager.NOTIFICATION, self.on_notification)


    def on_notification(self, data):
        
        message = data['message']
        title = data['title']
        if self.lastMessage != message:

            self.lastMessage = message
            
            if self.notif == None:
        
                if Notify.init(APPNAME):
                    self.notif = Notify.Notification.new(title, message, None)
                    self.notif.set_urgency(Notify.Urgency.LOW)
                    self.set_icon(data)
                    self.notif.set_timeout(Notify.EXPIRES_DEFAULT)
                    self.notif.show()
                else:
                    self.log.error('Error: there was a problem initializing the pynotify module')
            
            else:
                self.set_icon(data)
                self.notif.update(title, message, None)
                self.notif.show()


    def set_icon(self, data):
        #some radios publish cover data in the 'homepage' tag
        if('icon' in list(data.keys())):

            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(data['icon'], 48, 48)
                self.notif.set_icon_from_pixbuf(pixbuf)
            except Exception as e:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(APP_ICON, 48, 48)
                self.notif.set_icon_from_pixbuf(pixbuf)
                print(e)
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(APP_ICON, 48, 48)
            self.notif.set_icon_from_pixbuf(pixbuf)
