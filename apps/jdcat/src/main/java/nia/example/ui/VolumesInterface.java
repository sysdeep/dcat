package nia.example.ui;

import java.util.ArrayList;

import nia.example.core.models.Volume;
import nia.example.lib.Subject;

public interface VolumesInterface extends Subject {
    static String event_open_storage = "Open storage";

    public ArrayList<Volume> get_volumes();

    public void select_volume(Volume volume);
}
