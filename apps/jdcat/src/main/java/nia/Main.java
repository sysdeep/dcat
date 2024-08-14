package nia;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import nia.ui.Controller;
import nia.ui.MainWindow;
import nia.storage.LiteStorage;
import nia.storage.Storage;

public class Main {
    static Logger logger = LogManager.getRootLogger();

    public static void main(String[] args) {

        Storage storage = new LiteStorage();
        // storage.ping();
        // storage.open("/home/igor/1.gcat");

        Controller ctrl = new Controller(storage);

        // enable anti-aliased text:
        System.setProperty("awt.useSystemAAFontSettings", "on");

        new MainWindow(ctrl);
    }
}