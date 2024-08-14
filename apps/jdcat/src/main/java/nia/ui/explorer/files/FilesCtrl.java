package nia.ui.explorer.files;

import java.util.List;

import org.apache.logging.log4j.Logger;

import java.util.ArrayList;

import nia.core.models.FileRecord;
import nia.core.models.Volume;
import nia.lib.Log;
import nia.lib.Observer;
import nia.storage.Storage;
import nia.ui.Controller;

public class FilesCtrl implements FilesInterface {
    Storage _storage;
    Volume _volume;
    ArrayList<FileRecord> _files;
    private List<Observer> _observers;
    FileRecord _current_file;
    Logger _log;

    public FilesCtrl(Storage storage) {
        this._storage = storage;
        this._observers = new ArrayList<>();
        this._files = new ArrayList<>();

        this._log = Log.get_logger(Controller.class.toString());

    }

    // interface --------------------------------------------------------------
    @Override
    public ArrayList<FileRecord> get_files() {
        return this._files;
    }

    @Override
    public void set_volume(Volume volume) {
        System.out.println("Files ctrl: set_volume: " + volume.name);
        _volume = volume;
        _current_file = null;
        _files = _storage.get_volume_files(_volume.id, true);

        notifyObservers(list_changed);
    }

    @Override
    public void set_file(FileRecord record) {
        _log.info("selected file: " + record.name);
        _current_file = record;
        _files = _storage.get_files(_current_file.id);
        notifyObservers(list_changed);
    }

    // observer ---------------------------------------------------------------
    @Override
    public void register(Observer obj) {
        if (obj == null)
            throw new NullPointerException("Null Observer");

        if (!_observers.contains(obj))
            _observers.add(obj);
    }

    @Override
    public void unregister(Observer obj) {
        this._observers.remove(obj);
    }

    @Override
    public void notifyObservers(String event) {
        for (Observer obs : _observers) {
            obs.update(event);
        }
    }

}
