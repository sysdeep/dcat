package nia.example.lib;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Log {
    static Logger logger = LogManager.getRootLogger();

    static public Logger get_logger() {

        return Log.logger;
    }

    static public Logger get_logger(String name) {

        return LogManager.getLogger(name);
    }
}
