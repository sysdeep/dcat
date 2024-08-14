package nia.ui.explorer.volumes;

import java.util.ArrayList;
import java.util.List;

import nia.core.models.Volume;
import nia.lib.Observer;
import nia.storage.Storage;
import nia.ui.explorer.files.FilesInterface;

public class VolumesCtrl implements VolumesInterface {
    Storage _storage;
    FilesInterface _files_ctrl;
    List<Observer> _observers;

    public VolumesCtrl(Storage storage, FilesInterface files_ctrl) {
        this._storage = storage;
        this._files_ctrl = files_ctrl;
        this._observers = new ArrayList<>();
    }

    // interface --------------------------------------------------------------
    @Override
    public ArrayList<Volume> get_volumes() {
        return this._storage.get_volumes();
    }

    public void select_volume(Volume volume) {
        System.out.println("ctrl - select volume: " + volume.name);
        _files_ctrl.set_volume(volume);
    }

    // self -------------------------------------------------------------------
    public void reload() {
        notifyObservers(volumes_changed);
    }

    // --- oserver ------------------------------------------------------------
    @Override
    public void register(Observer obj) {
        if (obj == null)
            throw new NullPointerException("Null Observer");

        if (!_observers.contains(obj))
            _observers.add(obj);
    }

    @Override
    public void unregister(Observer obj) {
        _observers.remove(obj);
    }

    @Override
    public void notifyObservers(String event) {
        for (Observer obs : _observers) {
            obs.update(event);
        }
    }

}
