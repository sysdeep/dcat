package nia.ui.actions_bar;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JPanel;

public class ActionsBarView extends JPanel implements ActionListener {
    JButton _exit_button;

    public ActionsBarView() {
        _exit_button = new JButton("Exit");
        _exit_button.addActionListener(this); // назначаем обработчик события

        this.setLayout(new FlowLayout(FlowLayout.RIGHT));

        this.add(_exit_button);
    }

    // обработчик события, метод интерфейса ActionListener
    @Override
    public void actionPerformed(ActionEvent arg0) {
        // if (arg0.getActionCommand().equals("Add text"))
        // jta.append(" Add text\\n");
        // if (arg0.getActionCommand().equals("Clear text"))
        // jta.setText("");

        // если ссылки на объекты сохранены можно сравнивать
        // по объектам, например для JButton jbOK= new JBUtton("Ok");
        // то сравнение будет таким

        if (arg0.getSource().equals(_exit_button)) {
            System.exit(0);
        }
    }

}
