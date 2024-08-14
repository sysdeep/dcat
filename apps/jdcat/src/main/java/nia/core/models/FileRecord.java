package nia.core.models;

public class FileRecord {
    public static final Integer TYPE_FILE = 1;
    public static final Integer TYPE_DIR = 2;

    public String id;
    public String name;
    public Integer type;

    public FileRecord(String id, String name, Integer type) {
        this.id = id;
        this.name = name;
        this.type = type;
    }
}
