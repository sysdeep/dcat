package nia.example.ui;

import java.util.ArrayList;
import java.util.List;

import nia.example.core.models.Volume;
import nia.example.lib.Observer;
import nia.example.storage.Storage;

public class VolumesCtrl implements VolumesInterface {
    Storage storage;
    FilesInterface files_ctrl;

    // https://www.digitalocean.com/community/tutorials/observer-design-pattern-in-java
    private List<Observer> observers;

    public VolumesCtrl(Storage storage, FilesInterface files_ctrl) {
        this.storage = storage;
        this.observers = new ArrayList<>();
        this.files_ctrl = files_ctrl;
    }

    @Override
    public ArrayList<Volume> get_volumes() {
        return this.storage.get_volumes();
    }

    public void select_volume(Volume volume) {
        System.out.println("ctrl - select volume: " + volume.name);
        this.files_ctrl.set_volume(volume);
    }

    // --- oserver ------------------------------------------------------------
    @Override
    public void register(Observer obj) {
        if (obj == null)
            throw new NullPointerException("Null Observer");

        if (!observers.contains(obj))
            observers.add(obj);
    }

    @Override
    public void unregister(Observer obj) {
        observers.remove(obj);
    }

    @Override
    public void notifyObservers() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'notifyObservers'");
    }

}
