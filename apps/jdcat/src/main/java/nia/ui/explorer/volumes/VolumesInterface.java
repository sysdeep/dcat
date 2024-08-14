package nia.ui.explorer.volumes;

import java.util.ArrayList;

import nia.core.models.Volume;
import nia.lib.Subject;

public interface VolumesInterface extends Subject {
    static final String volumes_changed = "volumes_changed";

    public ArrayList<Volume> get_volumes();

    public void select_volume(Volume volume);
}
