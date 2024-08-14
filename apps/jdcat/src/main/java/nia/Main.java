package nia;

// import org.apache.logging.log4j.LogManager;
// import org.apache.logging.log4j.Logger;

import nia.ui.Controller;
import nia.ui.MainWindow;
import nia.storage.LiteStorage;
import nia.storage.Storage;

public class Main {
    // static Logger logger = LogManager.getRootLogger();

    public static void main(String[] args) {

        // System.out.println("=======================");
        // for (String a : args) {
        // System.out.println(a);
        // }
        // System.out.println("=======================");

        Storage storage = new LiteStorage();
        // storage.ping();
        // storage.open("/home/igor/1.gcat");

        Controller ctrl = new Controller(storage);

        // enable anti-aliased text:
        System.setProperty("awt.useSystemAAFontSettings", "on");

        new MainWindow(ctrl);

        if (args.length > 0) {
            ctrl.open_db(args[0]);
        }

        System.out.println("finish");
    }
}