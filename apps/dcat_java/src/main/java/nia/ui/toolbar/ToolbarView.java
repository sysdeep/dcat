package nia.ui.toolbar;

import java.awt.FlowLayout;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class ToolbarView extends JPanel {
    public ToolbarView() {
        JLabel title_label = new JLabel("Toolbar");

        JButton action_1_button = new JButton("Action 1");

        this.setLayout(new FlowLayout(FlowLayout.LEFT));

        this.add(title_label);
        this.add(action_1_button);
    }
}
