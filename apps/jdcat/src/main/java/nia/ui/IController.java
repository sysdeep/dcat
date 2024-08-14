package nia.ui;

import java.util.ArrayList;

import nia.core.models.FileRecord;
import nia.core.models.Volume;

public interface IController {
    public ArrayList<Volume> get_volumes();

    public ArrayList<FileRecord> get_volume_files(String volume_id, Boolean is_root);

    public VolumesInterface get_volumes_ctrl();

    public FilesInterface get_files_ctrl();

    public void open_db(String db_path);
}
