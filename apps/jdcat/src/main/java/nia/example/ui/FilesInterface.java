package nia.example.ui;

import java.util.ArrayList;

import nia.example.core.models.FileRecord;
import nia.example.core.models.Volume;
import nia.example.lib.Subject;

public interface FilesInterface extends Subject {
    static String event_volume_selected = "event_volume_selected";

    public ArrayList<FileRecord> get_volume_files(String volume_id);

    public ArrayList<FileRecord> get_files(String parent_id);

    public void set_volume(Volume volume);

    public Volume get_volume();
}
