package nia.ui.explorer.volumes;

import java.util.ArrayList;
import java.awt.Dimension;
// import java.awt.Font;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;
// import javax.swing.JLabel;

import nia.core.models.Volume;
import nia.lib.Observer;

public class VolumesViewExample {

    public static void main(String[] args) {

        // enable anti-aliased text:
        System.setProperty("awt.useSystemAAFontSettings", "on");

        VolumesControllerMock volumes_ctrl = new VolumesControllerMock();

        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame();

            VolumesView view = new VolumesView(volumes_ctrl);
            // view.setFont(new Font("ubuntu", Font.PLAIN, 18));

            // JLabel label = new JLabel("Example");
            // label.setFont(new Font("ubuntu", Font.PLAIN, 18));

            // frame.add(label);
            frame.add(view);

            frame.setPreferredSize(new Dimension(800, 400));
            frame.pack();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setVisible(true);

            // start
            volumes_ctrl.start();
        });

    }

}

class VolumesControllerMock implements VolumesInterface {
    ArrayList<Volume> _volumes;
    ArrayList<Observer> _observers;
    Volume _selected_volume;

    public VolumesControllerMock() {
        _volumes = new ArrayList<>();
        for (int i = 0; i < 13; i++) {

            Volume v = new Volume();
            v.id = Integer.toString(i);
            v.name = "volume " + v.id;
            _volumes.add(v);
        }

        _observers = new ArrayList<>();
    }

    public void start() {
        notifyObservers(volumes_changed);
    }

    @Override
    public void register(Observer obj) {
        _observers.add(obj);
    }

    @Override
    public void unregister(Observer obj) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'unregister'");
    }

    @Override
    public void notifyObservers(String event) {
        for (Observer obs : _observers) {
            obs.update(event);
        }
    }

    @Override
    public ArrayList<Volume> get_volumes() {
        return _volumes;
    }

    @Override
    public void select_volume(Volume volume) {
        _selected_volume = volume;
    }

}
