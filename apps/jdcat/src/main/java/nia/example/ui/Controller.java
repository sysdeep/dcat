package nia.example.ui;

import java.util.ArrayList;

import org.apache.logging.log4j.Logger;

import nia.example.core.models.FileRecord;
import nia.example.core.models.Volume;
import nia.example.lib.Log;
import nia.example.storage.Storage;

public class Controller implements IController {
    Storage _storage;
    Logger _log;
    VolumesCtrl volumes_ctrl;
    FilesCtrl files_ctrl;

    public Controller(Storage storage) {
        this._log = Log.get_logger(Controller.class.toString());
        this._storage = storage;

        this.files_ctrl = new FilesCtrl(storage);
        this.volumes_ctrl = new VolumesCtrl(storage, this.files_ctrl);
    }

    public ArrayList<Volume> get_volumes() {
        return this._storage.get_volumes();
    }

    @Override
    public void open_db(String db_path) {
        _log.info("open db: " + db_path);
    }

    @Override
    public ArrayList<FileRecord> get_volume_files(String volume_id, Boolean is_root) {
        return _storage.get_volume_files(volume_id, is_root);
    }

    public VolumesInterface get_volumes_ctrl() {
        return this.volumes_ctrl;
    }

    public FilesInterface get_files_ctrl() {
        return this.files_ctrl;
    }

}
