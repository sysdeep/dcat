package nia.example.ui;

import java.util.List;
import java.util.ArrayList;

import nia.example.core.models.FileRecord;
import nia.example.core.models.Volume;
import nia.example.lib.Observer;
import nia.example.storage.Storage;

public class FilesCtrl implements FilesInterface {
    Storage storage;
    Volume volume;
    private List<Observer> observers;

    public FilesCtrl(Storage storage) {
        this.storage = storage;
        this.observers = new ArrayList<>();

    }

    public ArrayList<FileRecord> get_volume_files(String volume_id) {
        return this.storage.get_volume_files(volume_id, true);
    }

    public ArrayList<FileRecord> get_files(String parent_id) {
        return this.storage.get_files(parent_id);
    }

    @Override
    public void register(Observer obj) {
        if (obj == null)
            throw new NullPointerException("Null Observer");

        if (!observers.contains(obj))
            observers.add(obj);
    }

    @Override
    public void unregister(Observer obj) {
        this.observers.remove(obj);
    }

    @Override
    public void notifyObservers() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'notifyObservers'");
    }

    @Override
    public void set_volume(Volume volume) {
        System.out.println("Files ctrl: set_volume: " + volume.name);
        this.volume = volume;

        for (Observer obs : this.observers) {
            obs.update(FilesInterface.event_volume_selected);
        }
    }

    @Override
    public Volume get_volume() {
        return this.volume;
    }

}
