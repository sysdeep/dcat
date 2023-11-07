package nia.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import nia.example.ui.Controller;
import nia.example.ui.MainWindow;
import nia.example.storage.LiteStorage;
import nia.example.storage.Storage;

public class Main {
    static Logger logger = LogManager.getRootLogger();

    public static void main(String[] args) {

        Storage storage = new LiteStorage();
        storage.ping();
        storage.open("/home/igor/1.gcat");

        Controller ctrl = new Controller(storage);

        new MainWindow(ctrl);
    }
}