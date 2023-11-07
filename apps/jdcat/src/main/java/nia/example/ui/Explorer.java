package nia.example.ui;

import javax.swing.JPanel;
import java.awt.BorderLayout;
import java.awt.FlowLayout;

public class Explorer extends JPanel {
    private VolumesView volumes_frame;
    private FilesView files_frame;

    public Explorer(IController controller) {

        this.volumes_frame = new VolumesView(controller.get_volumes_ctrl());
        this.files_frame = new FilesView(controller.get_files_ctrl());

        this.setLayout(new FlowLayout());
        // Container c = getContentPane(); // клиентская область окна
        // c.setLayout(new BorderLayout()); // выбираем компоновщик
        // // метку наверх
        this.add(volumes_frame, BorderLayout.WEST);
        this.add(files_frame, BorderLayout.EAST);
    }
}
