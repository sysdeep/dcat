package nia.storage;

import java.util.ArrayList;

import nia.core.models.FileRecord;
import nia.core.models.Volume;

public interface Storage {

    // public Repository get_repository(){

    // }

    public void open(String db_path);

    public void ping();

    public Volume get_volume();

    public ArrayList<Volume> get_volumes();

    public ArrayList<FileRecord> get_volume_files(String volume_id, Boolean is_root);

    public ArrayList<FileRecord> get_files(String parent_id);
}
