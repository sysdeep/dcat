package nia.ui.explorer.files;

import java.util.ArrayList;

import nia.core.models.FileRecord;
import nia.core.models.Volume;
import nia.lib.Subject;

public interface FilesInterface extends Subject {
    static String list_changed = "list_changed";

    // public ArrayList<FileRecord> get_volume_files();

    public ArrayList<FileRecord> get_files();

    public void set_volume(Volume volume);

    // public Volume get_volume();

    public void set_file(FileRecord record);
}
